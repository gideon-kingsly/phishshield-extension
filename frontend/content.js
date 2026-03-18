// Pre-click warning: intercept link clicks before navigation
document.addEventListener("click", (e) => {
  const link = e.target.closest("a");
  if (!link || !link.href) return;

  const url = link.href;

  // Ask background to check phishing before navigation
  chrome.runtime.sendMessage(
    { action: "precheck_url", url },
    (response) => {
      if (response && response.isPhishing) {
        e.preventDefault(); // stop navigation

        const reasonsText = (response.reasons || []).join("\n• ");
        const msg = `⚠️ Phishing Warning!\n\nThis link may be dangerous:\n${url}\n\nReasons:\n• ${reasonsText}\n\nDo you want to continue?`;

        const proceed = confirm(msg);

        if (proceed) {
          window.location.href = url; // allow navigation if user insists
        }
      }
    }
  );
}, true); // capture phase to intercept early