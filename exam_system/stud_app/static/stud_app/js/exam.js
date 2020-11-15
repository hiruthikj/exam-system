formsubmitted = false;
window.onbeforeunload = function(){
    if (!formsubmitted)
        return '';
};