document.addEventListener("DOMContentLoaded", () => {
  let postLikeArr = document.querySelectorAll(".hidden");
  postLikeArr.forEach((post) => {
    post.addEventListener("click", () => {
      let csrf = $("input[name=csrfmiddlewaretoken]").val();
      let postID = post.id;
      let url = `/total`;
      $.ajax({
        url: url,
        type: "post",
        data: {
          post_id: postID,
          csrfmiddlewaretoken: csrf,
        },
        success: (response) => {
          try {
            document.querySelector("#wait").remove();
          } catch {}

          const likeElement = document.createElement("div");
          likeElement.id = "wait";
          likeElement.innerHTML = `Total Like: ${response.count}<br>`;
          document
            .querySelector(`[id=${CSS.escape(postID)}]`)
            .append(likeElement);
        },
      });
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  let commentArr = document.querySelectorAll(".comment");
  commentArr.forEach((comment) => {
    comment.addEventListener("click", () => {
      let postID = comment.id;
      document.querySelector(`[class=${CSS.escape(postID)}]`).style.display =
        "none";
      document.querySelector(`[class=${CSS.escape(postID)}]`).style.display =
        "block";
    });
  });
});
