from sanic import Request
from co6co_sanic_ext.model.res.result import Result
from ..base_view import AuthMethodView
from ...services import fileService
import os


class RenameView(AuthMethodView):
    routePath = "/rename"

    async def post(self, request: Request):
        """
        重命名 文件或者目录
        @param {path:D:\\abcc\\xxx.xx,name:xxx.txt}
        """
        path_param = request.json.get("path", None)
        name = request.json.get("name", None)
        if path_param is None or name is None:
            return self.response_json(Result.fail(message="path和name参数是必须的"))
        try:
            os.renames(path_param, os.path.join(os.path.dirname(path_param), name))
            return self.response_json(Result.success(message="重命名完成！"))
        except Exception as e:
            return self.response_json(Result.fail(message="重命名失败{}".format(e)))
