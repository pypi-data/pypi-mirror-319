from locatr import (
    LocatrSeleniumSettings,
    PluginType,
    LlmSettings,
    LlmProvider,
    LocatrCdpSettings,
    Locatr,
    LocatrAppiumSettings,
)

llm_settings = LlmSettings(
    llm_provider=LlmProvider.OPENAI,
    llm_api_key="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",
    model_name="gpt-4o",
    reranker_api_key="UcucwL3ch7SQOQoAUsjrCiNrUuaD9AogUi31JP7p",
)
# locatr_settings_selenium = LocatrSeleniumSettings(
#     plugin_type=PluginType.SELENIUM,
#     llm_settings=llm_settings,
#     selenium_url="http://localhost:4444/wd/hub",
#     selenium_session_id="60c5d5af8779ff5e6949019abbaf2efc",
#     use_cache=False,
# )

locatr_settins_cdp = LocatrCdpSettings(
    llm_settings=llm_settings,
    cdp_url="http://localhost:9222",
)
# locatr_settings_appium = LocatrAppiumSettings(
#     llm_settings=llm_settings,
#     appium_url="http://172.30.192.1:4723/",
#     appium_session_id="6c6d19ff-2ec2-4c86-a112-9e09f2064615",
# )

lib = Locatr(locatr_settins_cdp, debug=True)
print(lib.get_locatr('Link to the first link'))
