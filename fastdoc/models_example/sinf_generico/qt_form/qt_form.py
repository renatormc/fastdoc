import fastdoc.gui_app.widgets as wt
from fastdoc.gui_app.widgets.swidget import SWidget


def convert_pericia(value):
    parts = value.split("/")
    return {"seq": int(parts[0]), "rg": int(parts[1]), "ano": int(parts[2])}


def convert_relatores(value):
    return [item.strip() for item in value.split(",")]


widgets: list[list[SWidget]] = [
    [
        wt.SText("pericia", required=True, label="Perícia",
                 placeholder="ex: 123/123465/2021", stretch=1, converter=convert_pericia),
        wt.SText("requisitante", required=True,
                 label="Requisitante", stretch=1),
        wt.SText("procedimento", required=True,
                 label="procedimento", stretch=1),
        wt.SText("ocorrencia_odin", label="Ocorrência do ODIN", stretch=1),
    ],
    [
        wt.SDate("data_odin", label="Data Odin"),
        wt.SDate("inicio_exame", label="Data de início do exame"),
        wt.SDate("data_recebimento", label="Data de recebimento"),
    ],
    [
        wt.SText("n_quesito", label="Número do quesito"),
        wt.SText("autoridade", label="Autoridade"),
    ],
    [
        wt.SStringList("relatores", label="Relatores",
                 placeholder="Entre os relatores separados por vírgula"),
        wt.SText("revisor", label="Revisor"),
    ],
    [
        wt.SText("lacre_entrada", label="Lacre de entrada"),
        wt.SText("lacre_saida", label="Lacre de saída")
    ],
    [
        wt.SStringList("pessoas_envolvidas", label="Pessoas envolvidas", placeholder="Pessoas separadas por vírgula")
    ],
    [
        wt.SObjetctsByPics("objects", label="Pasta com fotos dos objetos", default_object_type="Celular", object_types_choices=['Celular', 'Outro', 'Computador', 'Tablet', 'HDD'])
    ]

]
