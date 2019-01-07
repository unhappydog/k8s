--主要用于描述插件参数的数据格式.
-- bashboard页面上创建时需要填写的内容和添加插件时进行的校验


-- 引入模块,赋值table给typedefs变量
local typedefs = require "kong.db.schema.typedefs"

-- 自定义局部函数
local is_present = function(v)
  return type(v) == "string" and #v > 0   -- # 表示取长度
end


return {
  -- 插件名称
  name = "request-termination",

  fields = {
    { run_on = typedefs.run_on_first },
    { config = {
        type = "record",
      -- 描述插件参数的数据格式，用于 Kong 验证参数
        fields = {
          { status_code = {
            type = "integer",
            default = 503,
            between = { 100, 599 },
          }, },
          { message = { type = "string" }, },
          { content_type = { type = "string" }, },
          { body = { type = "string" }, },
        },
      -- 自定义更为细粒度的参数校验
        custom_validator = function(config)
          if is_present(config.message) and (is_present(config.content_type) or is_present(config.body))
          then
            return nil, "message cannot be used with content_type or body"
          end
          if is_present(config.content_type) and not is_present(config.body)
          then
            return nil, "content_type requires a body"
          end
          return true
        end,
      },
    },
  },
}
