"""
URLs pour le projet de nettoyage et analyse de données
"""

from django.urls import path

from clean_analyze.interface.view.deleteView import delete_dataset
from clean_analyze.interface.view.getAllView import get_all_dataset
from clean_analyze.interface.view.getByIdView import get_dataset_by_id
from clean_analyze.interface.view.globalStatView import get_global_stats
from clean_analyze.interface.view.departementStat import get_department_stats
from clean_analyze.interface.view.subjectStat import get_subject_stats
from clean_analyze.interface.view.teacherStat import get_teacher_stats
from clean_analyze.interface.view.studentReport import get_student_report
from clean_analyze.interface.view.topFloats import get_top_flops
from clean_analyze.interface.view.uploadView import upload_dataset

urlpatterns = [
    path("upload/", upload_dataset, name="upload_dataset"),
    path("getAll/", get_all_dataset, name="get_all_dataset"),
    path("getById/<uuid:dataset_id>/", get_dataset_by_id, name="get_dataset_by_id"),
    path("globalStat/<uuid:dataset_id>/", get_global_stats, name="get_global_stats"),
    path("departementStat/<uuid:dataset_id>/", get_department_stats, name="get_department_stats"),
    path("subjectStat/<uuid:dataset_id>/<uuid:subject>/", get_subject_stats, name="get_subject_stats"),
    path("teacherStat/<uuid:dataset_id>/<uuid:teacher>/", get_teacher_stats, name="get_teacher_stats"),
    path("studentReport/<uuid:dataset_id>/<uuid:student_id>/", get_student_report, name="get_student_report"),
    path("topFlops/<uuid:dataset_id>/<uuid:category>/", get_top_flops, name="get_top_flops"),
    path("delete/<uuid:dataset_id>/", delete_dataset, name="delete_dataset"),
]