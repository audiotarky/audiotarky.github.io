loaded = false;
if (document.monetization) {
    document.monetization.addEventListener('monetizationprogress', ({ detail }) => {
        if (!loaded) {
            loaded = true
            requestId = detail.requestId
            console.log(detail)
            var authz = new Request('/session', { method: 'POST', body: requestId });
            fetch(authz)
        }
    })
}