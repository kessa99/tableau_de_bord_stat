"""
vue pour récupérer un dataset par son ID
"""

from django.views.decorators.csrf import csrf_exempt

from clean_analyze.domain.useCase.getDatasetByIDUseCase import GetDatasetByIDUseCase
from clean_analyze.interface.utils import standard_response

@csrf_exempt
def get_dataset_by_id(request):
    """
    Récupérer un dataset par son ID
    """
    if request.method != "GET":
        return standard_response(
            message="Veuillez envoyer une requête GET",
            status_str="failed"
        )
    
    dataset_id = request.GET.get("dataset_id")
    if not dataset_id:
        return standard_response(
            message="Veuillez fournir un ID de dataset",
            status_str="failed"
        )

    use_case = GetDatasetByIDUseCase()
    try:
        dataset = use_case.execute(dataset_id)
        return standard_response(
            message="Dataset trouvé avec succès",
            content=dataset,
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