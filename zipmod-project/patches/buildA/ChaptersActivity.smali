.class public Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "ChaptersActivity.java"


# instance fields
.field private categoryJson:Ljava/lang/String;

.field private courseName:Ljava/util/ArrayList;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/ArrayList<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private extra:Ljava/util/ArrayList;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/ArrayList<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private jsonUrl:Ljava/lang/String;

.field private mAdView1:Lcom/google/android/gms/ads/AdView;

.field private recyclerView:Landroidx/recyclerview/widget/RecyclerView;

.field private serial:Ljava/util/ArrayList;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/ArrayList<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field

.field private templateView2:Lcom/google/android/ads/nativetemplates/TemplateView;

.field private title:Ljava/lang/String;


# direct methods
.method public constructor <init>()V
    .locals 1

    .line 28
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    .line 34
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->courseName:Ljava/util/ArrayList;

    .line 35
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->serial:Ljava/util/ArrayList;

    .line 36
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->extra:Ljava/util/ArrayList;

    return-void
.end method

.method private processData(Ljava/lang/String;)V
    .locals 6

    .line 85
    sget v0, Lcom/tarun/sscchslpreviousyearpapers/R$id;->shimmerContainer:I

    invoke-virtual {p0, v0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/FrameLayout;

    const/16 v1, 0x8

    .line 87
    invoke-virtual {v0, v1}, Landroid/widget/FrameLayout;->setVisibility(I)V

    .line 88
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->recyclerView:Landroidx/recyclerview/widget/RecyclerView;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Landroidx/recyclerview/widget/RecyclerView;->setVisibility(I)V

    .line 89
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->courseName:Ljava/util/ArrayList;

    invoke-virtual {v0}, Ljava/util/ArrayList;->clear()V

    .line 90
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->serial:Ljava/util/ArrayList;

    invoke-virtual {v0}, Ljava/util/ArrayList;->clear()V

    .line 91
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->extra:Ljava/util/ArrayList;

    invoke-virtual {v0}, Ljava/util/ArrayList;->clear()V

    if-nez p1, :cond_0

    .line 94
    const-string p1, "data not loading"

    invoke-static {p0, p1, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p1

    invoke-virtual {p1}, Landroid/widget/Toast;->show()V

    return-void

    .line 98
    :cond_0
    :try_start_0
    new-instance v0, Lorg/json/JSONArray;

    invoke-direct {v0, p1}, Lorg/json/JSONArray;-><init>(Ljava/lang/String;)V

    .line 101
    new-instance p1, Ljava/util/ArrayList;

    invoke-direct {p1}, Ljava/util/ArrayList;-><init>()V

    .line 102
    new-instance v2, Ljava/util/ArrayList;

    invoke-direct {v2}, Ljava/util/ArrayList;-><init>()V

    .line 103
    new-instance v3, Ljava/util/ArrayList;

    invoke-direct {v3}, Ljava/util/ArrayList;-><init>()V

    .line 105
    :goto_0
    invoke-virtual {v0}, Lorg/json/JSONArray;->length()I

    move-result v4

    if-ge v1, v4, :cond_1

    .line 106
    invoke-virtual {v0, v1}, Lorg/json/JSONArray;->getJSONObject(I)Lorg/json/JSONObject;

    move-result-object v4

    .line 107
    const-string v5, "name"

    invoke-virtual {v4, v5}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {p1, v5}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 108
    const-string v5, "series"

    invoke-virtual {v4, v5}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v2, v5}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 109
    const-string v5, "extra"

    invoke-virtual {v4, v5}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 111
    :cond_1
    new-instance v0, Lcom/tarun/sscchslpreviousyearpapers/Adapter;

    invoke-direct {v0, p1, v2, v3, p0}, Lcom/tarun/sscchslpreviousyearpapers/Adapter;-><init>(Ljava/util/ArrayList;Ljava/util/ArrayList;Ljava/util/ArrayList;Landroid/content/Context;)V

    .line 112
    iget-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->recyclerView:Landroidx/recyclerview/widget/RecyclerView;

    invoke-virtual {p1, v0}, Landroidx/recyclerview/widget/RecyclerView;->setAdapter(Landroidx/recyclerview/widget/RecyclerView$Adapter;)V
    :try_end_0
    .catch Lorg/json/JSONException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_1

    :catch_0
    move-exception p1

    .line 115
    invoke-virtual {p1}, Lorg/json/JSONException;->printStackTrace()V

    :goto_1
    return-void
.end method

.method private updateActionBar(Ljava/lang/String;I)V
    .locals 2

    .line 66
    sget v0, Lcom/tarun/sscchslpreviousyearpapers/R$id;->toolbar:I

    invoke-virtual {p0, v0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroidx/appcompat/widget/Toolbar;

    .line 67
    invoke-virtual {p0, v0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->setSupportActionBar(Landroidx/appcompat/widget/Toolbar;)V

    .line 69
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getSupportActionBar()Landroidx/appcompat/app/ActionBar;

    move-result-object v1

    if-eqz v1, :cond_0

    .line 70
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getSupportActionBar()Landroidx/appcompat/app/ActionBar;

    move-result-object v1

    invoke-virtual {v1, p1}, Landroidx/appcompat/app/ActionBar;->setTitle(Ljava/lang/CharSequence;)V

    .line 71
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getSupportActionBar()Landroidx/appcompat/app/ActionBar;

    move-result-object p1

    const/4 v1, 0x1

    invoke-virtual {p1, v1}, Landroidx/appcompat/app/ActionBar;->setDisplayHomeAsUpEnabled(Z)V

    .line 74
    sget p1, Lcom/tarun/sscchslpreviousyearpapers/R$drawable;->ic_arrow_back_white_24dp:I

    invoke-virtual {v0, p1}, Landroidx/appcompat/widget/Toolbar;->setNavigationIcon(I)V

    :cond_0
    if-eqz v0, :cond_1

    .line 78
    invoke-virtual {v0, p2}, Landroidx/appcompat/widget/Toolbar;->setBackgroundColor(I)V

    .line 79
    new-instance p1, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity$$ExternalSyntheticLambda0;

    invoke-direct {p1, p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity$$ExternalSyntheticLambda0;-><init>(Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;)V

    invoke-virtual {v0, p1}, Landroidx/appcompat/widget/Toolbar;->setNavigationOnClickListener(Landroid/view/View$OnClickListener;)V

    const/4 p1, -0x1

    .line 80
    invoke-virtual {v0, p1}, Landroidx/appcompat/widget/Toolbar;->setTitleTextColor(I)V

    :cond_1
    return-void
.end method


# virtual methods
.method synthetic lambda$updateActionBar$0$com-tarun-sscchslpreviousyearpapers-ChaptersActivity(Landroid/view/View;)V
    .locals 0

    .line 79
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->onBackPressed()V

    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 2

    .line 41
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 42
    sget p1, Lcom/tarun/sscchslpreviousyearpapers/R$layout;->activity_chapters:I

    invoke-virtual {p0, p1}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->setContentView(I)V

    .line 44
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getWindow()Landroid/view/Window;

    move-result-object p1

    const/high16 v0, -0x80000000

    .line 45
    invoke-virtual {p1, v0}, Landroid/view/Window;->addFlags(I)V

    .line 46
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    sget v1, Lcom/tarun/sscchslpreviousyearpapers/R$color;->colorSecondary:I

    invoke-virtual {v0, v1}, Landroid/content/res/Resources;->getColor(I)I

    move-result v0

    invoke-virtual {p1, v0}, Landroid/view/Window;->setStatusBarColor(I)V

    .line 48
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getIntent()Landroid/content/Intent;

    move-result-object p1

    const-string v0, "title"

    invoke-virtual {p1, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    iput-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->title:Ljava/lang/String;

    .line 49
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getIntent()Landroid/content/Intent;

    move-result-object p1

    const-string v0, "name"

    invoke-virtual {p1, v0}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    iput-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->categoryJson:Ljava/lang/String;

    .line 51
    iget-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->title:Ljava/lang/String;

    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getResources()Landroid/content/res/Resources;

    move-result-object v0

    sget v1, Lcom/tarun/sscchslpreviousyearpapers/R$color;->colorSecondary:I

    invoke-virtual {v0, v1}, Landroid/content/res/Resources;->getColor(I)I

    move-result v0

    invoke-direct {p0, p1, v0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->updateActionBar(Ljava/lang/String;I)V

    .line 52
    sget p1, Lcom/tarun/sscchslpreviousyearpapers/R$id;->madView2:I

    invoke-virtual {p0, p1}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Lcom/google/android/gms/ads/AdView;

    iput-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->mAdView1:Lcom/google/android/gms/ads/AdView;

    .line 53
    invoke-static {p1, p0}, Lcom/tarun/sscchslpreviousyearpapers/ads/Admob;->setBanner(Lcom/google/android/gms/ads/AdView;Landroid/content/Context;)V

    .line 56
    sget p1, Lcom/tarun/sscchslpreviousyearpapers/R$id;->recyclerView8:I

    invoke-virtual {p0, p1}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->findViewById(I)Landroid/view/View;

    move-result-object p1

    check-cast p1, Landroidx/recyclerview/widget/RecyclerView;

    iput-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->recyclerView:Landroidx/recyclerview/widget/RecyclerView;

    const/4 v0, 0x1

    .line 58
    invoke-virtual {p1, v0}, Landroidx/recyclerview/widget/RecyclerView;->setHasFixedSize(Z)V

    .line 59
    iget-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->recyclerView:Landroidx/recyclerview/widget/RecyclerView;

    new-instance v0, Landroidx/recyclerview/widget/LinearLayoutManager;

    invoke-direct {v0, p0}, Landroidx/recyclerview/widget/LinearLayoutManager;-><init>(Landroid/content/Context;)V

    invoke-virtual {p1, v0}, Landroidx/recyclerview/widget/RecyclerView;->setLayoutManager(Landroidx/recyclerview/widget/RecyclerView$LayoutManager;)V

    .line 62
    iget-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->categoryJson:Ljava/lang/String;

    invoke-direct {p0, p1}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->processData(Ljava/lang/String;)V

    return-void
.end method

.method public onOptionsItemSelected(Landroid/view/MenuItem;)Z
    .locals 2

    .line 121
    invoke-interface {p1}, Landroid/view/MenuItem;->getItemId()I

    move-result v0

    const v1, 0x102002c

    if-ne v0, v1, :cond_0

    .line 122
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->onBackPressed()V

    const/4 p1, 0x1

    return p1

    .line 125
    :cond_0
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onOptionsItemSelected(Landroid/view/MenuItem;)Z

    move-result p1

    return p1
.end method


# --- Added by ZIP mod: handler for the "Download All as ZIP" button (activity_chapters.xml) ---
.method public onZipButtonClick(Landroid/view/View;)V
    .locals 3

    # v1 = papers JSON array (intent extra "name", exactly what the original list uses)
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getIntent()Landroid/content/Intent;

    move-result-object v0

    const-string v1, "name"

    invoke-virtual {v0, v1}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    # v0 = section/year name (intent extra "title")
    invoke-virtual {p0}, Lcom/tarun/sscchslpreviousyearpapers/ChaptersActivity;->getIntent()Landroid/content/Intent;

    move-result-object v0

    const-string v2, "title"

    invoke-virtual {v0, v2}, Landroid/content/Intent;->getStringExtra(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    # ZipHelper.startZip(activity, section, papersJson)
    invoke-static {p0, v0, v1}, Lcom/zipmod/ZipHelper;->startZip(Landroid/app/Activity;Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method
