from datasette import hookimpl

PLUGIN_NAME = "datasette-auth-headers"
ID_HEADER_CONFIG_KEY = "id-header-name"


@hookimpl
def actor_from_request(datasette, request):
    conf = datasette.plugin_config(PLUGIN_NAME)
    if conf is None or type(conf) != dict:
        raise ValueError(
            f"configuration for {PLUGIN_NAME} was either missing or a non-dictionary type"
        )

    target_header_name = conf.get(ID_HEADER_CONFIG_KEY)
    if target_header_name is None or type(target_header_name) != str:
        raise ValueError(
            f"id_header_name {PLUGIN_NAME} was either missing or a non-str type"
        )

    target_header_name = target_header_name.lower()

    if hval := request.headers.get(target_header_name):
        return {"id": hval}
