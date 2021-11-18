export function expressCallback(controller) {
  return async (req, res) => {
    const httpRequest = {
      body: req.body,
      user: req.user,
      query: req.query,
      params: req.params,
      ip: req.ip,
      method: req.method,
      path: req.path,
      headers: {
        'Content-Type': req.get('Content-Type'),
        'Referer': req.get('referer'),
        'User-Agent': req.get('User-Agent'),
      },
      cookies: req.cookies,
    };
    try {
      const httpResponse = await controller(httpRequest);
      if (httpResponse.headers) {
        res.set(httpResponse.headers);
      }
      if (httpResponse.cookie) {
        res.cookie(httpResponse.cookie.name, httpResponse.cookie.value,
            httpResponse.cookie.options);
      }
      if (httpResponse.clearCookie) {
        res.clearCookie(httpResponse.clearCookie.name,
            httpResponse.clearCookie.options);
      }
      res.type('json');
      res.status(httpResponse.statusCode).send(httpResponse.body);
    } catch (error) {
      console.log(error);
      res.status(500).send({message: 'An unknown error occured'});
    }
  };
};
