from .exceptions import ServiceException
from threading import Thread
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpRequest

import re

class BaseService:
    modelo = None
    objeto = None

    create_fields = []
    update_fields = []
    serialize_fields = []
    foreign_fields = []
    unique_fields = []
    filter_fields = []
    sort_fields = []

    def __init__(self, id=None):
        if id is not None:
            self.set_objeto(id)
    
    def get_service(self):
        """
        Método que devuelve la instancia de este mismo servicio.
        """
        return self
            
    def set_objeto(self, id):
        try:
            self.objeto = self.modelo.objects.get(id=id)

        except self.modelo.DoesNotExist:
            raise ServiceException(f"El {self.modelo.__name__} con id '{id}' no existe.")
            
    def asincrono(self, funcion, *args):
        thread = Thread(target=funcion, args=args)
        thread.start()

    def check_objeto(self):
        if self.objeto is None:
            raise ServiceException(f"El {self.modelo.MODELO_SINGULAR.lower()} no ha sido definido.")

    def is_campo_image(self, campo):
        tipo = self.modelo._meta.get_field(campo).get_internal_type()
        return tipo == 'ImageField' or tipo == 'FileField'

    def get_valor_by_campo(self, campo):
        if campo in list(map(lambda x: x['campo'], self.foreign_fields)):
            foreign_field = list(filter(lambda x: x['campo'] == campo, self.foreign_fields))[0]

            if getattr(self.objeto, campo) is None:
                return None

            service = BaseService()
            service.modelo = getattr(self.objeto, campo)._meta.model
            service.objeto = getattr(self.objeto, campo)
            service.serialize_fields = foreign_field['serialize_fields']
            service.foreign_fields = foreign_field['foreign_fields'] if 'foreign_fields' in foreign_field else []

            return service.get_serializado()

        elif self.is_campo_image(campo):
            valor = getattr(self.objeto, campo)

            if valor:
                return valor.url

            return None

        else:
            return getattr(self.objeto, campo)

    def get_serializado(self):
        self.check_objeto()

        data = {}

        for campo in self.serialize_fields:
            valor = self.get_valor_by_campo(campo)
            data[campo] = valor

        return data
    
    def get_filtro_by_campo(self, campo, valor):
        if type(valor) == str:
            valor = valor.lower()

        if campo in list(map(lambda x: x['campo'], self.foreign_fields)):
            campo = campo + '_id'
            return {campo: valor}

        filtro_icontains = f'{campo}__icontains'

        return {filtro_icontains: valor}

    def listar(self, request: HttpRequest, page=None, page_size=None, filter=None, sort=None):
        data = []
        
        filters = filter if filter else {}
        sorts = sort if sort else {}
    
        # Aplicar filtros
        if filters:
            for campo, valor in filters.items():
                # Asegúrate de que estos filtros sean válidos según tu modelo
                filtro = self.get_filtro_by_campo(campo, valor)
                filters.update(filtro)
    
        # Obtener los objetos filtrados
        objetos = self.modelo.objects.filter(**filters)
    
        # Aplicar ordenamiento
        if sorts:
            order_by_fields = [
                f"{'' if direccion == 'asc' else '-'}{campo}"
                for campo, direccion in sorts.items()
            ]
            objetos = objetos.order_by(*order_by_fields)
    
        # Si page o page_size es None, devolver solo data y total
        if page is None or page_size is None:
            for objeto in objetos:
                service = self.__class__()
                service.objeto = objeto
                data.append(service.get_serializado())
            return {
                "data": data,
                "total": objetos.count(),
            }
    
        # Configurar el paginador
        paginator = Paginator(objetos, page_size)
    
        try:
            paginated_objects = paginator.page(page)
        except PageNotAnInteger:
            paginated_objects = paginator.page(1)
        except EmptyPage:
            paginated_objects = paginator.page(paginator.num_pages)
    
        # Serializar los objetos paginados
        for objeto in paginated_objects:
            service = self.__class__()
            service.objeto = objeto
            data.append(service.get_serializado())
    
        # Obtener la URL base de la solicitud (para paginación)
        base_url = request.build_absolute_uri(request.path)
    
        # Generar URLs de next y previous
        previous_url = None
        next_url = None
    
        if paginated_objects.has_previous():
            previous_url = f"{base_url}&page={paginated_objects.previous_page_number()}&page_size={page_size}"
    
        if paginated_objects.has_next():
            next_url = f"{base_url}&page={paginated_objects.next_page_number()}&page_size={page_size}"
    
        # Retornar datos paginados con metadatos
        return {
            "data": data,
            "total": paginator.count,
            "page": paginated_objects.number,
            "num_pages": paginator.num_pages,
            "page_size": page_size,
            "previous": previous_url,
            "next": next_url,
        }
    
                    
    def validar_unicidad(self, campo, valor):
        if campo in self.unique_fields:
            if self.modelo.objects.filter(**{campo: valor}).exists():
                raise ServiceException(f"El campo '{campo}' con valor '{valor}' ya existe.")
            

    def crear(self, **kwargs):
        objeto = self.modelo()

        for campo in self.create_fields:
            if campo not in kwargs:
                raise ServiceException(f"El campo '{campo}' es requerido para crear.")
            
            valor = kwargs[campo]
            
            self.validar_unicidad(campo, valor)

            if campo in list(map(lambda x: x['campo'], self.foreign_fields)):
                campo = campo + '_id'

            setattr(objeto, campo, valor)

        objeto.save()
        self.objeto = objeto


    def actualizar(self, **kwargs):
        self.check_objeto()

        for campo, valor in kwargs.items():
            if campo == 'id':
                continue

            if campo not in self.update_fields:
                raise ServiceException(f"El campo '{campo}' no es un campo válido para actualizar.")
            
            self.validar_unicidad(campo, valor)

            if campo in list(map(lambda x: x['campo'], self.foreign_fields)):
                campo = campo + '_id'

            setattr(self.objeto, campo, valor)

        self.objeto.save()

    def eliminar(self):
        self.check_objeto()

        self.objeto.delete()
        self.objeto = None

        