from django.db.models import Q, QuerySet
from catalog_app.models import Good, Category, Compilation, CompilationItem


def fetch_all_goods() -> QuerySet[Good]:
    queryset = Good.objects.all()
    return queryset


def search_goods(search: str) -> QuerySet[Good]:
    queryset = Good.objects.filter(Q(name__icontains=search) | Q(art__icontains=search))
    return queryset


def fetch_all_categories() -> QuerySet[Category]:
    queryset = Category.objects.filter(parent=None).all()
    return queryset


def fetch_subcategories(parent: Category) -> QuerySet[Category]:
    queryset = Category.objects.filter(parent=parent).all()
    return queryset


def fetch_category_by_slug(slug: str) -> Category | None:
    return Category.objects.filter(slug=slug).first()


def fetch_compilation_by_slug(slug: str) -> Compilation | None:
    return Compilation.objects.filter(slug=slug).first()


def fetch_compilations_by_category(category: Category) -> QuerySet[Compilation]:
    return Compilation.objects.filter(category=category).all()


def fetch_universal_compilations() -> QuerySet[Compilation]:
    return Compilation.objects.filter(category=None).all()


def fetch_categories_by_ids(ids: list[str]) -> QuerySet[Category]:
    return Category.objects.filter(id__in=ids).all()


def fetch_good_by_slug(slug: str) -> Good | None:
    return Good.objects.filter(slug=slug).first()


def fetch_goods_by_slugs(slugs: list[str]) -> list[Good] | None:
    return Good.objects.filter(slug__in=slugs).all()


def fetch_goods_by_category(category: Category) -> QuerySet[Good]:
    queryset = Good.objects.filter(category=category).all()
    return queryset


def fetch_goods_by_compilation(compilation: Compilation) -> QuerySet[Good]:
    ids = [
        str(item.good.id)
        for item in CompilationItem.objects.filter(compilation=compilation).all()
    ]
    return fetch_goods_by_ids(ids=ids)


def fetch_goods_by_categories(categories: list[Category]) -> QuerySet[Good]:
    queryset = Good.objects.filter(category__in=categories).all()
    return queryset


def fetch_goods_by_ids(ids: list[str]) -> QuerySet[Good]:
    return Good.objects.filter(id__in=ids).all()


def create_or_update_goods(
    goods_to_create: list[Good], goods_to_update: list[Good]
) -> None:
    if goods_to_create:
        Good.objects.bulk_create(goods_to_create)
    if goods_to_update:
        Good.objects.bulk_update(
            goods_to_update,
            ["name", "art", "code", "okei", "price", "balance", "k", "description"],
        )
