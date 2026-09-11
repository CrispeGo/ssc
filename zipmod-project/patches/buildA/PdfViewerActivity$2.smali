.class Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;
.super Ljava/lang/Object;
.source "PdfViewerActivity.java"

# interfaces
.implements Lcom/downloader/OnDownloadListener;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->showDownloadDialog()V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

.field final synthetic val$downloadDir:Ljava/io/File;


# direct methods
.method constructor <init>(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;Ljava/io/File;)V
    .locals 0
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x1010
        }
        names = {
            null,
            null
        }
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "()V"
        }
    .end annotation

    .line 188
    iput-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    iput-object p2, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->val$downloadDir:Ljava/io/File;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onDownloadComplete()V
    .locals 4

    .line 191
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    invoke-static {v0}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$200(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;)Landroid/app/Dialog;

    move-result-object v0

    invoke-virtual {v0}, Landroid/app/Dialog;->dismiss()V

    .line 192
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    new-instance v1, Ljava/io/File;

    iget-object v2, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->val$downloadDir:Ljava/io/File;

    iget-object v3, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    invoke-static {v3}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$300(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;)Ljava/lang/String;

    move-result-object v3

    invoke-direct {v1, v2, v3}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    invoke-static {v0, v1}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$002(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;Ljava/io/File;)Ljava/io/File;

    .line 193
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    invoke-static {v0}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$000(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;)Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->exists()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 194
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    invoke-static {v0}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$000(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;)Ljava/io/File;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$100(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;Ljava/io/File;)V

    # --- ZIP mod: also export a user-accessible copy to Downloads (additive) ---
    iget-object v0, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    invoke-static {v0}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$000(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;)Ljava/io/File;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/zipmod/ZipHelper;->exportIndividualPdf(Landroid/content/Context;Ljava/io/File;)V

    :cond_0
    return-void
.end method

.method public onError(Lcom/downloader/Error;)V
    .locals 2

    .line 200
    iget-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    invoke-static {p1}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->access$200(Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;)Landroid/app/Dialog;

    move-result-object p1

    invoke-virtual {p1}, Landroid/app/Dialog;->dismiss()V

    .line 201
    iget-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    const-string v0, "Download failed"

    const/4 v1, 0x0

    invoke-static {p1, v0, v1}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object p1

    .line 202
    invoke-virtual {p1}, Landroid/widget/Toast;->show()V

    .line 203
    iget-object p1, p0, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity$2;->this$0:Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;

    invoke-virtual {p1}, Lcom/tarun/sscchslpreviousyearpapers/PdfViewerActivity;->finish()V

    return-void
.end method
