Thought for 3s
CSS
- Drop this into your main stylesheet or inside a <style> block.

:root{
  --c-bg:#ffffff;
  --c-fg:#0f172a;      /* neutral dark */
  --c-muted:#94a3b8;   /* muted gray */
  --c-primary:#0ea5e9; /* brand */
  --c-accent:#22d3ee;  /* accent */
}

label.checkbox{
  display:inline-flex;
  align-items:center;
  gap:10px;
  cursor:pointer;
  user-select:none;
  color:var(--c-fg);
}

label.checkbox:hover{ opacity:0.97; }

/* Switch base */
label.checkbox > input[type="checkbox"]{
  appearance:none;
  -webkit-appearance:none;
  width:44px;
  height:26px;
  border-radius:999px;
  border:1px solid rgba(15,23,42,0.15);
  background:rgba(15,23,42,0.08);
  position:relative;
  outline:none;
  transition:background .2s ease, border-color .2s ease, box-shadow .2s ease;
}

/* Knob */
label.checkbox > input[type="checkbox"]::after{
  content:"";
  position:absolute;
  top:2px; left:2px;
  width:22px; height:22px;
  border-radius:50%;
  background:#fff;
  box-shadow:0 1px 2px rgba(0,0,0,0.15);
  transition:transform .2s ease;
}

/* Checked state */
label.checkbox > input[type="checkbox"]:checked{
  background:var(--c-primary);
  border-color:var(--c-primary);
}
label.checkbox > input[type="checkbox"]:checked::after{
  transform:translateX(18px);
}

/* Focus ring for accessibility */
label.checkbox > input[type="checkbox"]:focus-visible{
  box-shadow:0 0 0 3px color-mix(in oklab, var(--c-accent) 38%, transparent);
}

/* Text styling */
label.checkbox > span{
  font-weight:500;
  color:var(--c-fg);
  transition:color .2s ease;
}
label.checkbox > input[type="checkbox"]:checked + span{
  color:var(--c-primary);
}

/* Tiny bump animation on toggle */
@keyframes bump{ 0%{transform:scale(1)} 50%{transform:scale(0.94)} 100%{transform:scale(1)} }
label.checkbox.toggled > input[type="checkbox"]::after{ animation:bump .18s ease }

/* Optional badges if you add spans with these classes */
.badge{
  display:inline-block; padding:2px 8px; border-radius:999px;
  font-size:12px; line-height:1; background:rgba(15,23,42,0.06); color:var(--c-fg);
}
.badge.on{ background:color-mix(in oklab, var(--c-primary) 20%, #fff); color:var(--c-fg); }
.badge.off{ background:rgba(15,23,42,0.06); color:var(--c-muted); }

/* Optional lifestyle/RAF preview styling */
#lifestyle-risk, #raf-preview{
  font-weight:600; color:var(--c-fg);
}

JavaScript
- Place before </body> or in your bundle. It:
  - Updates state/animation
  - Computes lifestyle risk increment (smoking=+0.20, alcohol=+0.10)
  - Updates optional #lifestyle-risk and #raf-preview elements if present
  - Optionally autosaves via POST (commented; enable when your endpoint exists)

<script>
(function(){
  const smoking = document.querySelector('label.checkbox > input[name="smoking"]');
  const alcohol = document.querySelector('label.checkbox > input[name="alcohol"]');

  function computeLifestyleRisk(smokes, drinks){
    // Match your RAF logic: +0.20 for smoking, +0.10 for alcohol
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

  bind(smoking);
  bind(alcohol);
  updatePreviews();
})();
</script>

Optional markup for previews and badges
- Add these near your fields if you want visual feedback without hitting the server:
- <div> Lifestyle risk: <span id="lifestyle-risk">0.00</span> </div>
- <div> RAF preview: <span id="raf-preview" data-base-raf="0.00">0.00</span> </div>
- <span class="badge on" style="display:none"></span>  if you choose to drive extra badges 

This drops in with your existing HTML, provides a smooth switch UI, updates lifestyle risk immediately, and is ready to autosave once your backend route is available.