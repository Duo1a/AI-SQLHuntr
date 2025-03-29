修复方案

---

### **输入过滤**

$username = filter_input(INPUT_POST, 'username',FILTER_SANITIZE_STRING);

### **使用最小权限原则**

数据库账户应限制为仅能执行必要的操作，避免使用具有管理员权限的账户连接数据库。如果应用程序只需要读取权限，就不要赋予写入权限。

### **错误信息处理**

禁止在生产环境中显示详细的数据库错误信息，因为这些信息可能包含有关数据库结构的重要线索。应该记录错误并显示通用错误消息。

`if ($mysqli->connect_error) {     die('Database connection error'); }`

### **启用Web应用防火墙（WAF）**

使用Web应用防火墙（如ModSecurity）可以有效检测和阻止常见的SQL注入攻击。

### **限制数据库的字符集**

限制数据库字符集为UTF-8，并防止SQL注入攻击者通过特殊字符来进行攻击。

---
