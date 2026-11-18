import logging
import time


logger = logging.getLogger('academia.auditoria')


class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        inicio = time.monotonic()
        response = self.get_response(request)
        duracion = (time.monotonic() - inicio) * 1000
        logger.info(
            'HTTP %s | Ruta: %s | Estado: %s | %.2f ms',
            request.method,
            request.path,
            response.status_code,
            duracion
        )
        return response
