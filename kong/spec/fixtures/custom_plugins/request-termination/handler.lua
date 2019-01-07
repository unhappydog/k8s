-- 执行函数. 按照配置返回固定的响应


-- 引入模块(引入基类)
local BasePlugin = require "kong.plugins.base_plugin"
local singletons = require "kong.singletons"
local constants = require "kong.constants"
local meta = require "kong.meta"

-- 局部变量
local kong = kong
local server_header = meta._SERVER_TOKENS

-- 默认的response
local DEFAULT_RESPONSE = {
  [401] = "Unauthorized",
  [404] = "Not found",
  [405] = "Method not allowed",
  [500] = "An unexpected error occurred",
  [502] = "Bad Gateway",
  [503] = "Service unavailable",
}

-- 扩展模块(派生子类),其实这里是为了继承来自 Classic 的 __call 元方法，方便 Kong 在 init 阶段预加载插件的时候执行构造函数 new()
local RequestTerminationHandler = BasePlugin:extend()

-- 设置插件的优先级，Kong 将按照插件的优先级来确定其执行顺序（越大越优先）
-- 需要注意的是应用于 Consumer 的插件因为依赖于 Auth，所以 Auth 类插件优先级普遍比较高
RequestTerminationHandler.PRIORITY = 2
RequestTerminationHandler.VERSION = "1.0.0"

-- 插件的构造函数，用于初始化插件的 _name 属性，后面会根据这个属性打印插件名
-- 其实这个方法不是必须的，只是用于插件调试
function RequestTerminationHandler:new()
  RequestTerminationHandler.super.new(self, "request-termination")
end

-- 表明需要在 access 阶段执行此插件. 也就是在接入上游服务前就直接生成响应数据.
function RequestTerminationHandler:access(conf)   -- conf就是schema.lua中的config,也就是插件安装时的配置页面
  -- 执行父类的 access 方法，其实就是为了调试时输出日志用的
  RequestTerminationHandler.super.access(self)

  -- 接下来的就是插件的主要逻辑
  local status  = conf.status_code
  local content = conf.body
 -- 如果配置了content参数
  if content then
    local headers = {
      ["Content-Type"] = conf.content_type
    }

    if singletons.configuration.enabled_headers[constants.HEADERS.SERVER] then
      headers[constants.HEADERS.SERVER] = server_header
    end

    return kong.response.exit(status, content, headers)
  end
  -- 如果没有配置content参数,就直接生成message的消息体
  return kong.response.exit(status, { message = conf.message or DEFAULT_RESPONSE[status] })
end


return RequestTerminationHandler
