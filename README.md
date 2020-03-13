# ProductBigDataAPITesting
自动化API测试项目

目录  
- 1、生成测试用例  
- 2、查看测试用例  
- 3、执行测试用例  
- 4、查看测试结果  

## 生成测试用例
向数据库写入测试用例，用例格式：  
`{
host：主机,
url：测试API,
request：请求数据,
result：预计结果,
}`





## 查看测试用例
查询数据库中已存在的测试用例





## 执行测试用例
选择某些测试用例并执行




## 查看测试结果
测试结果数据格式：
{
test_code:测试编号
test_username:测试用户名称
testcase_id:测试用例id
testcase_result:测试用例返回结果
testcase_recode:测试用例返回码(200/404)
testcase_count:测试次数
create_at:测试时间
}