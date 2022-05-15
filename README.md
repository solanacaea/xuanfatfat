## 小胖按键
>永久免费，目前已支持多按键脚本  
>小胖从驱动层模拟按键，理论上任何游戏都可以使用  

#### --------------v0.2 更新-----------------  
1. 支持大写字母按键  
2. Unhandled exception in script, NameError: name 'exit' is not defined  
3. 记录历史按键  
#### --------------v0.3 更新-----------------  
1. 兼容Win7操作系统  
2. 修复重新打开小胖，加载上一次设置的按键值不起作用的问题
#### --------------v0.4 更新-----------------  
1. 多按键功能上线
2. 钓鱼、多点挖矿/采药、攻防等脚本

## 常见问题
### 1. 驱动启动错误  
可能是操作系统禁用了小胖签名导致无法启动驱动程序。  
1) 通过“设置”打开高级启动，打开开始菜单或开始屏幕，选择“设置”  
	或按 Win + i 组合键打开“设置”  
2) 单击“更新和安全 -> 恢复”，在右侧的“高级启动”部分，单击“立即重新启动”  
	或“Windows安全更新”->“高级选项”-> "恢复" -> “高级重启”  
3) 电脑重新启动，然后进入高级启动画面  
“选择一个选项”->“疑难解答”->“高级选项”->“重启设置”界面点击“重启”按钮 ->启动设置界面按“7”禁用驱动程序强制签名  
4) 重启后再次运行小胖  
5) 特别提示：禁用驱动强制签名后，存在被黑客利用该漏洞攻击的风险（一般小人物的电脑黑客看不上），建议安装杀毒软件或者别在这台电脑上不良网站
### 2. 无法启动此程序，因为计算机中丢失api-ms-win-core-path-l1-1-0.ddl。
Win7系统可能遇到这个问题，从下面链接下载该文件，然后复制到C:\Windows\System32\，64位系统为：C:\Windows\SysWOW64
https://cn.dll-files.com/api-ms-win-core-path-l1-1-0.dll.html

### 3. 其它未知错误
可能需要安装C++依赖，下载地址：https://www.microsoft.com/zh-cn/download/details.aspx?id=48145

## 下载方式
1. 找到<Code>下拉框
	![image](https://user-images.githubusercontent.com/43092492/168454120-27ac8aef-6de6-442a-9ebc-076c81afc9e8.png)
2. 选<Download ZIP>
![image](https://user-images.githubusercontent.com/43092492/168454042-24cd9af2-0926-408a-966e-24eca32326b3.png)


## 特别感谢
DD虚拟按键：http://www.ddxoft.com/  
源码地址：https://github.com/ddxoft

## 欢迎大家提改进建议
联系方式：jx3_xiaopang@126.com
