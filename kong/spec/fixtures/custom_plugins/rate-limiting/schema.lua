
-- 引入数据库类型
local typedefs = require "kong.db.schema.typedefs"


local ORDERED_PERIODS = { "second", "minute", "hour", "day", "month", "year"}


-- 自定义参数校验函数
local function validate_periods_order(config)
  for i, lower_period in ipairs(ORDERED_PERIODS) do
    local v1 = config[lower_period]
    if type(v1) == "number" then
      for j = i + 1, #ORDERED_PERIODS do
        local upper_period = ORDERED_PERIODS[j]
        local v2 = config[upper_period]
        if type(v2) == "number" and v2 < v1 then
          return nil, string.format("The limit for %s(%.1f) cannot be lower than the limit for %s(%.1f)",
                                    upper_period, v2, lower_period, v1)
        end
      end
    end
  end

  return true
end




return {
  name = "rate-limiting",
  fields = {
    { run_on = typedefs.run_on { one_of = { "first", "second" } } },
    { config = {
        type = "record",
        fields = {
          { second = { type = "number", gt = 0 }, },  --取值大于0
          { minute = { type = "number", gt = 0 }, },
          { hour = { type = "number", gt = 0 }, },
          { day = { type = "number", gt = 0 }, },
          { month = { type = "number", gt = 0 }, },
          { year = { type = "number", gt = 0 }, },
          { limit_by = {
              type = "string",
              default = "consumer",
              one_of = { "consumer", "credential", "ip" },   -- 可选择项
          }, },
          { policy = {
              type = "string",
              default = "cluster",
              len_min = 0,
              one_of = { "local", "cluster", "redis" },
          }, },
          { fault_tolerant = { type = "boolean", default = true }, },    --多选框
          { redis_host = typedefs.host },
          { redis_port = typedefs.port({ default = 6379 }), },
          { redis_password = { type = "string", len_min = 0 }, },
          { redis_timeout = { type = "number", default = 2000, }, },
          { redis_database = { type = "integer", default = 0 }, },
          { hide_client_headers = { type = "boolean", default = false }, },
        },
        custom_validator = validate_periods_order,    -- 自定义参数校验
      },
    },
  },
  -- 参数完整性校验,参数同时包含哪些内容
  entity_checks = {
    { at_least_one_of = { "config.second", "config.minute", "config.hour", "config.day", "config.month", "config.year" } },   -- 这些参数至少存在一个
    { conditional = {
      if_field = "config.policy", if_match = { eq = "redis" },    -- 如果 指定参数存在,且值为指定内容,  则 参数选项必须也存在
      then_field = "config.redis_host", then_match = { required = true },
    } },
    { conditional = {
      if_field = "config.policy", if_match = { eq = "redis" },    -- 如果 指定参数存在,且值为指定内容,  则 参数选项必须也存在
      then_field = "config.redis_port", then_match = { required = true },
    } },
    { conditional = {
      if_field = "config.policy", if_match = { eq = "redis" },    -- 如果 指定参数存在,且值为指定内容,  则 参数选项必须也存在
      then_field = "config.redis_timeout", then_match = { required = true },
    } },
  },
}
