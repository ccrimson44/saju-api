# saju_logic.py

heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
earthly_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']

def calculate_fake_saju(year: int, month: int, day: int, time: str, calendar_type: str) -> str:
    year_stem = heavenly_stems[year % 10]
    year_branch = earthly_branches[year % 12]
    day_stem = heavenly_stems[day % 10]
    day_branch = earthly_branches[day % 12]

    result = (
        f"당신은 {calendar_type} 기준으로 {year}년 {month}월 {day}일 {time}시에 태어났습니다.\n"
        f"연주는 {year_stem}{year_branch}, 일주는 {day_stem}{day_branch}입니다.\n"
        f"오늘은 인간관계에 집중하면 좋은 날입니다."
    )
    return result
