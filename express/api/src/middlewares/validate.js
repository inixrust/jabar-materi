// Memvalidasi body, query, dan params dengan skema zod.
// Hasil yang sudah bersih tersedia di req.validated.{body,query,params}.
//
// Contoh pemakaian pada rute:
//   router.post('/', validate({ body: createProductSchema }), createProduct);
export function validate({ body, query, params } = {}) {
  return (req, _res, next) => {
    try {
      req.validated = {
        body: body ? body.parse(req.body) : undefined,
        query: query ? query.parse(req.query) : undefined,
        params: params ? params.parse(req.params) : undefined,
      };
      next();
    } catch (err) {
      next(err);
    }
  };
}
