from zeroconf import Zeroconf, ServiceInfo
import socket
import atexit

class LocalDNS:
    def __init__(self, service_name="MyDevice", service_type="_http._tcp.local.", ip=None, port=8080):
        """
        Zeroconf를 이용해 DNS 서비스를 관리하는 클래스.
        
        :param service_name: DNS 상에서 표시할 서비스 명 (예: "MyDevice")
        :param service_type: DNS 서비스 타입 (예: "_http._tcp.local.")
        :param ip: 등록하고자 하는 서비스 IP (None일 경우 내부 IP 자동 탐색)
        :param port: 서비스에 접속할 포트 번호 (예: 8080)
        """
        self.service_name = service_name
        self.service_type = service_type
        self.ip = ip or self._get_internal_ip()
        self.port = port
        self.zeroconf = Zeroconf()
        self.info = None

    def _get_internal_ip(self):
        """
        내부 IP 주소를 가져오는 비공개 메서드.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Google DNS 서버 사용
            internal_ip = s.getsockname()[0]
            s.close()
            return internal_ip
        except OSError:
            return None

    def register_service(self):
        """
        Zeroconf를 통해 DNS 서비스를 등록합니다.
        """
        if not self.ip:
            raise ValueError("유효한 IP 주소를 찾을 수 없습니다.")

        # 네트워크 바이트 오더로 IP 주소 변환
        address_bytes = socket.inet_aton(self.ip)

        # 풀 서비스 이름 생성
        full_service_name = f"{self.service_name}.{self.service_type}"

        # 기본 TXT 레코드 설정
        properties = {
            "description": "Example DNS service",
            "version": "1.0.0"
        }

        # ServiceInfo 객체 생성
        self.info = ServiceInfo(
            type_=self.service_type,
            name=full_service_name,
            addresses=[address_bytes],
            port=self.port,
            properties=properties,
            server=f"{self.service_name}.local."
        )
        self.zeroconf.register_service(self.info)
        atexit.register(self.cleanup)
        print(f"서비스 등록됨: {full_service_name} ({self.ip}:{self.port})")

    def cleanup(self):
        """
        Zeroconf 서비스를 해제합니다.
        """
        if self.info:
            self.zeroconf.unregister_service(self.info)
            self.info = None
            print("서비스가 해제되었습니다.")
        self.zeroconf.close()


if __name__ == "__main__":
    dns_service = LocalDNS(service_name="TestDevice", port=8080)
    dns_service.register_service()
