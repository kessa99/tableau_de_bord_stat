"""
vue pour récupérer tous les datasets
"""
from django.views.decorators.csrf import csrf_exempt

from clean_analyze.domain.useCase.getAllDatasetUseCase import GetAllDatasetUseCase
from clean_analyze.interface.utils import standard_response

@csrf_exempt
def get_all_dataset(request):
    """
    Récupérer tous les datasets
    """
    if request.method != "GET":
        return standard_response(
            message="Veuillez envoyer une requête GET",
            status_str="failed"
        )
    
    use_case = GetAllDatasetUseCase()
    try:
        datasets = use_case.execute()
        return standard_response(
            message="Tous les datasets trouvés avec succès",
            content=datasets,
            code=200,
            status_str="succes"
        )
    except Exception as e:
        return standard_response(
            message=str(e),
            content={},
            status_str="failed",
            code=500
        )