mkdir -p ${KONG_DIR}/custom_plugins/xxx/migrations
touch postgres.lua
return {
     {
         name = "xxxxxxxxx",
         up = [[
             CREATE TABLE IF NOT EXISTS ${TABLENAME}(
                 xx
             );
         ]],
         down = [[
             DROP TABLE ${TABLENAME};
         ]]
     }
 }
