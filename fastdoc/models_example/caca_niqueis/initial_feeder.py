from pathlib import Path
from typing import Optional, Union
from report_writer.types import InitialData
from fastdoc.data_extractors.odin_parser import OdinPdfParser
from fastdoc.data_extractors.sinfweb_bridge import get_pericia_data


def get_initial_data(workdir: Union[Path, str]) -> Optional[InitialData]:
    d = InitialData()
    d.form_data = {}
    path = Path(workdir) / "Requisicao.pdf"
    if path.exists():
        parser = OdinPdfParser(path)
        data = parser.extract_all()
        p = data.pericia
        d.form_data['pericia'] = f"{p.seq}/{p.rg}/{p.ano}"
        d.form_data['requisitante'] = data.quesito.unidade_origem
        d.form_data['procedimento'] = f"RAI {data.rai}"
        d.form_data['ocorrencia_odin'] = data.ocorrencia
        d.form_data['data_odin'] = data.data_ocorrencia
        d.form_data['numero_quesito'] = data.quesito.numero
        d.form_data['autoridade'] = data.autoridade
        data_sinfweb = get_pericia_data(p.rg, p.ano)
        d.form_data['relatores'] = data_sinfweb['relatores']
        if data_sinfweb['revisor']:
            d.form_data['revisores'] = [data_sinfweb['revisor']]
        d.form_data['inicio_exame'] = data_sinfweb['data_atribuicao'].split()[0]

    return d