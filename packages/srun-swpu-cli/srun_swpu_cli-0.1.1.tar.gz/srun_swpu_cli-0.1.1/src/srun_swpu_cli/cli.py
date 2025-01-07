import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from srun_swpu import Account, NetworkType, AccountFactory, LoginSession 

console = Console()

def create_parser():
    parser = argparse.ArgumentParser(description='校园网登录工具')
    parser.add_argument('action', choices=['login', 'logout', 'status'], help='要执行的操作')
    parser.add_argument('--student-id', help='学号', required=False)
    parser.add_argument('--network-type',
                        required=False,
                        choices=['china-mobile-wireless', 'china-mobile-wired', 'student', 'teacher', 'china-telecom-wireless'], 
                        help='网络类型')
    parser.add_argument('--password', help='密码（仅登录时需要）', required=False)
    return parser

def get_network_type(type_str):
    network_type_map = {
        'china-mobile-wireless': NetworkType.YD_WIRELESS,
        'china-mobile-wired': NetworkType.YD_WIRED,
        'student': NetworkType.STUDENT,
        'teacher': NetworkType.TEACHER,
        'china-telecom-wireless': NetworkType.TELECOM
    }
    return network_type_map[type_str]

def print_error(message: str):
    """打印错误信息"""
    console.print(Panel(
        Text(message, style="bold red"),
        title="错误",
        border_style="red"
    ))

def print_success(message: str):
    """打印成功信息"""
    console.print(Panel(
        Text(message, style="bold green"),
        title="成功",
        border_style="green"
    ))

def print_info(message: str):
    """打印信息"""
    console.print(Panel(
        Text(message, style="bold blue"),
        title="信息",
        border_style="blue"
    ))

def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.action == 'login':
            if not args.network_type:
                print_error("登录操作需要提供网络类型")
                sys.exit(1)
            network_type = get_network_type(args.network_type)
            if not args.password or args.password == "" or not args.student_id or args.student_id == "":
                print_error("登录操作需要提供账号密码")
                sys.exit(1)
            account = AccountFactory.create_account(args.student_id, network_type, args.password)
            
        elif args.action == 'logout':
            if not args.network_type:
                print_error("登录操作需要提供网络类型")
                sys.exit(1)
            network_type = get_network_type(args.network_type)
            if not args.student_id or args.student_id == "":
                print_error("注销操作需要提供账号")
                sys.exit(1)
            account = AccountFactory.create_account(args.student_id, network_type, "dummy_password")
            
        else:  
            account = AccountFactory.create_account("000000000000", NetworkType.STUDENT, "dummy_password")

        session = LoginSession(account)
        
        if args.action == 'login':
            response = session.login()
            if response.success:
                print_success(f"登录成功{'\n消息' + response.message if response.message else ''}")
                if response.policy_message:
                    print_info(f"策略消息: {response.policy_message}")
            else:
                print_error(f"登录失败{'\n消息' + response.message if response.message else ''}")
            
        elif args.action == 'logout':
            response = session.logout()
            if response.success:
                print_success(f"注销成功{'\n消息' + response.message if response.message else ''}")
            else:
                print_error(f"注销失败{'\n消息' + response.message if response.message else ''}")
            
        else:  # status
            response = session.get_status()
            if response.success and response.is_online:
                table = Table(title="在线状态", show_header=False, border_style="green")
                table.add_column("属性", style="cyan")
                table.add_column("值", style="green")
                
                table.add_row("用户名", response.username)
                table.add_row("IP地址", response.ip_address)
                table.add_row("MAC地址", response.mac_address)
                table.add_row("已用流量", response.format_used_traffic())
                table.add_row("在线时长", response.format_used_time())
                table.add_row("账户余额", str(response.balance))
                if response.domain:
                    table.add_row("网络类型", response.domain)
                    
                console.print(table)
            else:
                print_info("当前处于离线状态")
                if response.message:
                    print_info(f"消息: {response.message}")

    except ValueError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

if __name__ == '__main__':
    main() 