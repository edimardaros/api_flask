def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=5,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0, **dados):
  if cidade:
    return {
      'estrelas_min' : estrelas_min,
      'estelas_max': estrelas_max,
      'diaria_min' : diaria_min,
      'diaria_max' : diaria_max,
      'cidade': cidade,
      'limit': limit,
      'offset':offset
    }
  return {
      'estrelas_min' : estrelas_min,
      'estelas_max': estrelas_max,
      'diaria_min' : diaria_min,
      'diaria_max' : diaria_max,
      'limit': limit,
      'offset':offset
  }

consulta_sem_cidade = "SELECT * FROM hoteis \
      WHERE (estrelas >= %s and estrelas <= %s)\
        AND (diaria >= %s and diaria <= %s)\
          LIMIT %s OFFSET %s"


consulta_com_cidade = "SELECT * FROM hoteis \
      WHERE (estrelas >= %s and estrelas <= %s)\
        AND (diaria >= %s and diaria <= %s)\
        AND (cidade = %s)\
          LIMIT %s OFFSET %s"