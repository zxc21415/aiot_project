$(document).ready(function () {
    var pr = document.getElementsByName("PR");
    var fc = document.getElementsByName("F1");
    var move = document.getElementsByName("chart");
    $(pr).click(function (event) {
      if (pr[0].checked) {
        $("#img_PR").attr("src", "/static/img/chart/PR_20.jpg");
        $("#title_PR").text("Precision-Recall(權重20)");
      };
      if (pr[1].checked) {
        $("#img_PR").attr("src", "/static/img/chart/PR_30.jpg");
        $("#title_PR").text("Precision-Recall(權重30)");
      };
      if (pr[2].checked) {
        $("#img_PR").attr("src", "/static/img/chart/PR_40.jpg");
        $("#title_PR").text("Precision-Recall(權重40)");
      };
    });
    $(fc).click(function (event) {
      if (fc[0].checked) {
        $("#img_F1").attr("src", "/static/img/chart/F1_20.jpg");
        $("#title_F1").text("F1-Confidence(權重20)");
      };
      if (fc[1].checked) {
        $("#img_F1").attr("src", "/static/img/chart/F1_30.jpg");
        $("#title_F1").text("F1-Confidence(權重30)");
      };
      if (fc[2].checked) {
        $("#img_F1").attr("src", "/static/img/chart/F1_40.jpg");
        $("#title_F1").text("F1-Confidence(權重40)");
      };
    });
    $(move).change(function (event) {
      var to_div = "#chart" + move[0].options.selectedIndex;
      a = document.getElementById(to_div);
      a.scrollIntoView(true)
    });
    $('#BackTop').click(function () {
      a = document.getElementById("top");
      a.scrollIntoView(true);
    });
  });

//SHOW.HTML
$(document).ready(function () {
    $('#id_image').on('change', loadImgOnLable)

});

// 上傳圖片
function uploadImgA() {
    $("#id_image").trigger("click");

}

function loadImgOnLable(e) {
    var readFile = new FileReader();
    var mfile = $("#id_image")[0].files[0];  //注意這裡必須是$("#myfile")[0]，document.getElementById('file')等價與$("#myfile")[0]
    readFile.readAsDataURL(mfile);
    readFile.onload = function () {
        var img = $("#show");
        img.attr("src", this.result);
    }
}