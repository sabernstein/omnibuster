const toggleCommentIcon = ev => {
    const elem = ev.currentTarget;
    if (elem.innerHTML === '') {
        elem.innerHTML = `<i class="fa-regular fa-comment"></i> 
                            ${showCommentDetail}`
    } 
    else {
        elem.innerHTML = ''
    }
}

const showCommentDetail = ev => {
    const postId = ev.currentTarget.dataset.postId;
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post => {
            const html = `
                <div class="modal-bg">
                    <button id="x" onclick="destroyModal(event)" ><p><strong>X</strong></p></button>
                    <div class="modal">
                        <img src="${post.image_url}" />
                        <div class="modal_info">
                            <div id=user>
                                <img src=${ post.user.thumb_url } alt=${ post.caption }>
                                <p id="username"> <strong> ${ post.user.username } </strong></p>
                            </div>
                            <p id="comments"> <strong>${post.user.username}</strong> ${post.caption} </p>
                            <div> <p id="sug_for_u"> ${ post.display_time } </p> </div>
                            <div class="comments">
                                ${ showCommentsAll(post.comments) }
                            </div>
                        </div>
                    </div>
                </div>`;
            document.querySelector('#modal-container').innerHTML = html;
        })
    
};

const destroyModal = ev => {
    document.querySelector('#modal-container').innerHTML = "";
    document.querySelector(`#x`).focus();
};