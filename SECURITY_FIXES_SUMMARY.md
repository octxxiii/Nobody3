# 보안 취약점 수정 요약

## ✅ 수정 완료

### 1. SSL/TLS 인증서 검증 활성화
- **파일**: `Nobody/services/downloader.py`
- **변경**: `nocheckcertificate: False`, `prefer_insecure: False`
- **효과**: MITM 공격 방지, 안전한 HTTPS 연결 강제

### 2. 파일명 Sanitization 강화
- **파일**: `Nobody/utils/security.py` (신규)
- **함수**: `sanitize_filename()`
- **기능**:
  - Path traversal 방지 (`os.path.basename()`)
  - Windows 예약 문자 제거 (`<>:"|?*\`)
  - 유니코드 정규화
  - 파일명 길이 제한 (255자)
  - 제어 문자 제거

### 3. URL 검증 추가
- **파일**: `Nobody/utils/security.py` (신규)
- **함수**: `validate_url()`
- **기능**:
  - 허용된 프로토콜만 허용 (http, https)
  - SSRF 방지 (localhost, private IP 차단)
  - URL 형식 검증

### 4. 적용 위치
- `Nobody/services/downloader.py`: 파일명 sanitization 적용
- `Nobody/views/presenter.py`: URL 검증 적용

## 📋 남은 작업 (선택사항)

### 낮은 우선순위
1. FFmpeg 다운로드 무결성 검증 (SHA256 체크섬)
2. 임시 파일 처리 개선 (`try-finally` 블록)
3. 의존성 취약점 스캔 (`pip-audit` 또는 `safety`)

## ⚠️ 주의사항

### SSL 인증서 검증 활성화의 영향
일부 사이트에서 SSL 인증서 오류가 발생할 수 있습니다:
- 자체 서명 인증서를 사용하는 사이트
- 만료된 인증서를 사용하는 사이트
- 인증서 체인 문제가 있는 사이트

**해결 방법**:
- 사용자에게 경고 메시지 표시
- 특정 사이트에 대한 예외 처리 (신중하게)
- 인증서 오류 로깅

### URL 검증의 영향
일부 로컬 테스트나 특수한 URL이 차단될 수 있습니다:
- `localhost` URL
- Private IP 주소
- `file://` 프로토콜

**해결 방법**:
- 개발 모드에서 검증 비활성화 옵션
- 화이트리스트 기능 추가

## 테스트 권장사항

1. **SSL 인증서 검증 테스트**
   - 정상적인 YouTube/SoundCloud URL 테스트
   - 인증서 오류가 있는 사이트 테스트

2. **파일명 Sanitization 테스트**
   - 특수 문자가 포함된 제목 테스트
   - Path traversal 시도 (`../../../etc/passwd`)
   - 긴 파일명 테스트

3. **URL 검증 테스트**
   - 정상적인 URL 테스트
   - `file://` 프로토콜 시도
   - `localhost` URL 시도
   - Private IP 주소 시도

