# 최종 푸시 가이드

## ✅ 완료된 작업

1. ✅ `.gitignore` 업데이트
2. ✅ 파일 정리 및 커밋
3. ✅ 릴리즈 태그 생성 (`v2.0.0`)
4. ✅ main 브랜치로 병합 완료

## 🚀 GitHub에 푸시하기

### 1. 메인 브랜치 푸시

```bash
git push -u origin main
```

### 2. 태그 푸시

```bash
git push origin v2.0.0
```

또는 모든 태그:
```bash
git push origin --tags
```

## 📦 GitHub Releases 설정

푸시 완료 후:

1. https://github.com/octxxiii/Nobody3/releases 로 이동
2. "Draft a new release" 클릭
3. 태그: `v2.0.0` 선택
4. 제목: `Nobody 3 v2.0.0`
5. 릴리즈 노트 작성
6. `releases/Nobody3-Windows.zip` 업로드
7. "Publish release" 클릭

## ✅ 완료 확인

- [x] 커밋 완료
- [x] 태그 생성 완료
- [x] main 브랜치 병합 완료
- [ ] GitHub 푸시 (다음 단계)
- [ ] Releases 생성 (웹에서)

