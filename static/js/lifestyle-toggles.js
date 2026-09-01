(function(){
  // Find checkbox elements
  const smoking = document.querySelector('label.checkbox > input[name="smoking"]');
  const alcohol = document.querySelector('label.checkbox > input[name="alcohol"]');

  function computeLifestyleRisk(smokes, drinks){
    // Match RAF logic: +0.20 for smoking, +0.10 for alcohol
    return (smokes ? 0.20 : 0) + (drinks ? 0.10 : 0);
  }

  function updateLabelState(inputEl){
    const lbl = inputEl?.closest('label.checkbox');
    if (!lbl) return;
    lbl.dataset.state = inputEl.checked ? 'on' : 'off';
    lbl.classList.add('toggled');
    setTimeout(() => lbl.classList.remove('toggled'), 200);
  }

  // Optional: update preview elements if you include them in your template
  function updatePreviews(){
    const s = !!smoking?.checked;
    const a = !!alcohol?.checked;
    const lifestyle = computeLifestyleRisk(s, a); // 0..0.30

    const lifestyleEl = document.getElementById('lifestyle-risk');
    if (lifestyleEl) {
      lifestyleEl.textContent = lifestyle.toFixed(2); // show as 0.00
      lifestyleEl.dataset.value = String(lifestyle);
    }

    // If you have a base RAF value on the element (data-base-raf), add lifestyle component
    const rafEl = document.getElementById('raf-preview');
    if (rafEl) {
      const base = parseFloat(rafEl.dataset.baseRaf || '0');
      const raf = Math.min(1, Math.max(0, base + lifestyle));
      rafEl.textContent = raf.toFixed(2);
      rafEl.dataset.value = String(raf);
    }
  }

  // Optional: Debounced autosave to your backend (enable when your route exists)
  const debounce = (fn, ms=500) => {
    let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  };
  const autosave = debounce(async () => {
    try {
      // Example endpoint: adjust URL to your actual route (e.g., /profile/lifestyle)
      const res = await fetch('/profile/lifestyle', {
        method:'POST',
        headers:{ 'Content-Type':'application/json' },
        body: JSON.stringify({
          smoking: !!smoking?.checked,
          alcohol: !!alcohol?.checked
        }),
        credentials: 'include'
      });
      // console.log('[v0] autosave status', res.status);
    } catch(e){
      // console.log('[v0] autosave error', e);
    }
  }, 600);

  function bind(inputEl){
    if (!inputEl) return;
    // Initialize state on load
    updateLabelState(inputEl);
    inputEl.addEventListener('change', () => {
      updateLabelState(inputEl);
      updatePreviews();
      // autosave(); // uncomment when your endpoint is ready
    });
    // Optional keyboard bump for users toggling with space/enter
    inputEl.addEventListener('keyup', (e) => {
      if (e.key === ' ' || e.key === 'Enter') {
        const lbl = inputEl.closest('label.checkbox');
        if (!lbl) return;
        lbl.classList.add('toggled');
        setTimeout(() => lbl.classList.remove('toggled'), 200);
      }
    });
  }

  // Only bind if we're on a page with these elements
  if (smoking || alcohol) {
    bind(smoking);
    bind(alcohol);
    updatePreviews();
  }
})();