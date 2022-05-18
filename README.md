## 小胖按键
>永久免费，目前已支持多按键脚本  
>小胖从驱动层模拟按键，理论上任何游戏都可以使用  
### 界面
<img src="https://user-images.githubusercontent.com/43092492/169019857-92c1698f-787f-4806-bc9f-f8594683556c.png" width="250px">  <img src="https://user-images.githubusercontent.com/43092492/169019964-0239b51e-ed0b-493e-a565-a8d5cafaf12a.png" width="250px">  <img src="https://user-images.githubusercontent.com/43092492/169020019-8c4f8e05-22f6-4781-9037-20d2f0c32b73.png" width="250px">

## 常见问题
### 1. 驱动启动错误  
	小胖驱动程序没有经过微软签名认证，所以操作系统禁用了小胖签名导致无法启动驱动程序。 
##### 临时禁用强制签名
	1) 通过“设置”打开高级启动，打开开始菜单或开始屏幕，选择“设置”  
		或按 Win + i 组合键打开“设置”  
	2) 单击“更新和安全 -> 恢复”，在右侧的“高级启动”部分，单击“立即重新启动”
		或“Windows安全更新”->“高级选项”-> "恢复" -> “高级重启”  
	3) 电脑重新启动，然后进入高级启动画面  
		“选择一个选项”->“疑难解答”->“高级选项”->“重启设置”界面点击“重启”按钮 ->启动设置界面按“7”禁用驱动程序强制签名  
	4) 重启后再次运行小胖  
##### 永久禁用强制签名
	在开始菜单中输入cmd -> 以管理员身份运行 -> 在窗口输入：  
	bcdedit.exe /set nointegritychecks on  
	回车，若打印操作成功完成，重启即可永久禁用  
	
	如果提示：
	设置元素数据时出错。
	该值受安全引导策略保护，无法进行修改或删除。

	需要执行以下步骤：
	1) 通过“设置”打开高级启动，打开开始菜单或开始屏幕，选择“设置”  
		或按 Win + i 组合键打开“设置”  
	2) 单击“更新和安全 -> 恢复”，在右侧的“高级启动”部分，单击“立即重新启动”
		或“Windows安全更新”->“高级选项”-> "恢复" -> “高级重启”  
	3) 电脑重新启动，然后进入高级启动画面  
		“选择一个选项”->“疑难解答”->“高级选项”->UEFI固件设置  
		进入BIOS中，关闭安全启动。把“secure boot”设为“disable”  
		老操作系统界面：  
![image](https://user-images.githubusercontent.com/43092492/169016541-5846b6d1-9d18-4608-82a2-a679df23563d.png)  
		
		新操作系统界面：  
		BIOS启动设置 -> 启动选项 -> 安全启动模式 关闭  
	4) 重启完成后
		在开始菜单中输入cmd -> 以管理员身份运行 -> 在窗口输入：  
		bcdedit.exe /set nointegritychecks on  
##### 特别提示
	关闭该功能，对系统是有一定危险的哦
### 2. 无法启动此程序，因为计算机中丢失api-ms-win-core-path-l1-1-0.ddl。
	Win7系统可能遇到这个问题，从下面链接下载该文件，然后复制到C:\Windows\System32\，64位系统为：C:\Windows\SysWOW64  
	https://cn.dll-files.com/api-ms-win-core-path-l1-1-0.dll.html
### 3. 其它未知错误
	可能需要安装C++依赖，下载地址：https://www.microsoft.com/zh-cn/download/details.aspx?id=48145
### 更新日志
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
## 特别感谢
DD虚拟按键：http://www.ddxoft.com/  
源码地址：https://github.com/ddxoft
## 欢迎大家提改进建议
联系方式：jx3_xiaopang@126.com
