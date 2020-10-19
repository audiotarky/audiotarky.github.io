if (document.monetization) {
    let scale = false;
    let total = 0;
    let canFathom = false;

    function paymentGoals(ev) {
        total += Number(ev.detail.amount);

        if (total > 50000 && canFathom) {
            console.log('Goal sent: ' + total);
            // TODO: send the goal if a pointer changes
            if (ev.detail.paymentPointer.endsWith('WRPFhabhyrxF')) {
                window.fathom.trackGoal('LVTANHVF', 1);
            } else {
                window.fathom.trackGoal('70S0YWJD', 1);
            }
            total = 0;
        };
    };

    document.monetization.addEventListener(
        'monetizationprogress',
        paymentGoals
    );

    document.addEventListener(
        'DOMContentLoaded',
        function (e) {
            window.fathom.trackGoal('2QVO4MF4', 0);
            canFathom = true;
        }
    );
};
