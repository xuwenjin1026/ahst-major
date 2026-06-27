import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 确保能找到本地安装的 Django
libs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahst_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
django.setup()

from api.models import MajorScore, Major
from django.db.models import Count, Q

print("=" * 60)
print(" 历年分数线数据分布检查")
print("=" * 60)
print()

# 按年份分组统计
print("【按年份分布】")
year_stats = MajorScore.objects.values('year').annotate(
    count=Count('id'),
    physics=Count('id', filter=Q(subject_type='physics')),
    history=Count('id', filter=Q(subject_type='history'))
).order_by('year')

for stat in year_stats:
    print(f"  {stat['year']}年: 共 {stat['count']} 条（物理 {stat['physics']}, 历史 {stat['history']}）")

print()

# 检查每个专业的历年数据覆盖
print("【每个专业的历年覆盖】")
majors = Major.objects.all().order_by('id')
for major in majors:
    scores = MajorScore.objects.filter(major_id=major.id).order_by('year')
    years = [str(s.year) for s in scores]
    has_min = all(s.min_score is not None for s in scores)
    print(f"  {major.id:2d}. {major.name:20s} {major.subject_type:8s} "
          f"年份: {', '.join(years) if years else '(无数据)'}")

print()

# 检查数据字段完整性
print("【数据字段完整性 - 物理类最新年份样本】")
sample_scores = MajorScore.objects.filter(
    subject_type='physics'
).order_by('-year')[:5]
for s in sample_scores:
    print(f"  {s.year} {s.major.name:20s} "
          f"min={s.min_score}, max={s.max_score}, avg={s.avg_score}, "
          f"min_rank={s.min_rank}, max_rank={s.max_rank}, "
          f"plan={s.plan_count}, actual={s.actual_count}")

print()
print("【数据字段完整性 - 历史类最新年份样本】")
sample_scores = MajorScore.objects.filter(
    subject_type='history'
).order_by('-year')[:5]
for s in sample_scores:
    print(f"  {s.year} {s.major.name:20s} "
          f"min={s.min_score}, max={s.max_score}, avg={s.avg_score}, "
          f"min_rank={s.min_rank}, max_rank={s.max_rank}, "
          f"plan={s.plan_count}, actual={s.actual_count}")

print()
print("=" * 60)
