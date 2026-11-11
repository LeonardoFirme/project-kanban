document.addEventListener('contextmenu', function(e) { e.preventDefault(); });
document.addEventListener('keydown', function(e) {
    if (e.keyCode === 123) { e.preventDefault(); return false; }
    if (e.ctrlKey && e.shiftKey && [73, 74, 67].includes(e.keyCode)) { e.preventDefault(); return false; }
    if (e.ctrlKey && e.keyCode === 85) { e.preventDefault(); return false; }
    if (e.ctrlKey && e.keyCode === 83) { e.preventDefault(); return false; }
});