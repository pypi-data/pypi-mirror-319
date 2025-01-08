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
#     selenium_session_id="e4c543363b9000a66073db7a39152719",
# )
#
locatr_settins_cdp = LocatrCdpSettings(
    llm_settings=llm_settings,
    cdp_url="http://localhost:9222",
)
locatr_settings_appium = LocatrAppiumSettings(
    llm_settings=llm_settings,
    appium_url="http://172.30.192.1:4723/",
    appium_session_id="6c6d19ff-2ec2-4c86-a112-9e09f2064615",
)

lib = Locatr(locatr_settins_cdp, debug=True)
lib2 = Locatr(locatr_settins_cdp, debug=True)
print(lib.get_locatr("Give me locatr that shows the current time."), "here")
print(lib2.get_locatr("Give me locatr that shows the current time."), "here")
