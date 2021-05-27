import path_config
from mainapp.models import PricePolicy


def run():
    exists = PricePolicy.objects.filter(category=1, title="个人免费版").exists()
    if not exists:
        PricePolicy.objects.create(
            category=1,
            title="个人免费版",
            price=0,
            project_num=3,
            project_member=2,
            # 以M为单位
            project_space=20,
            per_file_size=5
        )


if __name__ == "__main__":
    run()