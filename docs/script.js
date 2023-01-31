function change_content(div_content) {
    const mediabox     = document.getElementById('mediabox');
    mediabox.innerHTML = div_content;
}



function main() {
    // Consants
    const eyebleach_path = '/Users/mark/Pictures/eyebleach';
    const img_exts       = ["png", "jpg", "jpeg", "webp"];
    const vid_exts       = ["mp4"];
    const files          = [
        "zuahe0dbk4991.png",
        "zpiup4nojgz81.png",
        "redditsave.com_vacuum-s0z2ez3pj1j91.mp4",
        "redditsave.com_under_siege-lxm1rxbh8e991.mp4"
    ];

    // Picks a random file
    let randi       = Math.floor(Math.random() * files.length);
    let filename    = files[randi];
    let filepath    = `${eyebleach_path}/${filename}`;
    document.title  = filename;

    // Gets the extension of the file
    let arr = filename.split('.');
    let ext = arr[arr.length-1];

    // Checks if its an image or video
    let div_content;
    if (img_exts.includes(ext)) {
        console.log(`image | ${filename}`);
        div_content = `<img class="center-fit" src="${filepath}">`;
    }
    else if (vid_exts.includes(ext)) {
        console.log(`video | ${filename}`);
        div_content = `<video controls autoplay class="center-fit"><source src="${filepath}" type="video/mp4"></video>`;
    }
    else {
        console.log(`huh? | ${filename}`);
        div_content = `huh?`;
    }

    // Runs change_content() once DOM has loaded
    window.onload = function() {
        change_content(div_content);
    };
}



main();