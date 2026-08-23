/* =========================================================
   FIREGUARD AI
   Frontend Controller
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       CONFIGURATION
    ===================================================== */

    const API_BASE = "https://fireguardai-qsd4.onrender.com";


    /* =====================================================
       ANIMATED STATISTICS
    ===================================================== */

    const counters = document.querySelectorAll(".stat-number");

    const animateCounter = (element) => {

        const target = Number(element.dataset.target || 0);

        let current = 0;

        const duration = 1800;
        const start = performance.now();

        const update = (time) => {

            const progress = Math.min(
                (time - start) / duration,
                1
            );

            const eased =
                1 - Math.pow(1 - progress, 3);

            current = Math.floor(target * eased);

            element.textContent =
                current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        };

        requestAnimationFrame(update);
    };


    if (counters.length > 0) {

        const observer = new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        animateCounter(entry.target);

                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.5
            }
        );

        counters.forEach((counter) => {
            observer.observe(counter);
        });
    }


    /* =====================================================
       NAVIGATION ACTIVE STATE
    ===================================================== */

    const navLinks =
        document.querySelectorAll(".nav-links a");

    navLinks.forEach((link) => {

        link.addEventListener("click", () => {

            navLinks.forEach((item) => {
                item.classList.remove("active");
            });

            link.classList.add("active");
        });
    });


    /* =====================================================
       MOUSE PARALLAX
    ===================================================== */

    const visual =
        document.querySelector(".hero-visual");

    if (visual) {

        document.addEventListener("mousemove", (event) => {

            const x =
                event.clientX / window.innerWidth - 0.5;

            const y =
                event.clientY / window.innerHeight - 0.5;

            visual.style.transform =
                `translate(${x * 8}px, ${y * 8}px)`;
        });
    }


    /* =====================================================
       BUTTON FEEDBACK
    ===================================================== */

    const buttons =
        document.querySelectorAll(
            ".primary-button, .secondary-button"
        );

    buttons.forEach((button) => {

        button.addEventListener("click", () => {

            button.style.transform = "scale(0.97)";

            setTimeout(() => {
                button.style.transform = "";
            }, 120);
        });
    });


    /* =====================================================
       AI ANALYST
    ===================================================== */

    /*
       We only activate this section when analyst.html
       elements are available.
    */

    const situationInput =
        document.querySelector(
            "#situation, #situationInput, textarea"
        );

    const regionInput =
        document.querySelector(
            "#region, #regionSelect, select[name='region']"
        );

    const modeInput =
        document.querySelector(
            "#analysisMode, #mode, #modeSelect, select[name='mode']"
        );


    /*
       Find the Run AI Analysis button.

       Supports:
       - #runAnalysis
       - #run-ai-analysis
       - .run-analysis
       - data-action buttons
       - arrow buttons used by the current UI
    */

    let runButton =
        document.querySelector(
            "#runAnalysis, #run-ai-analysis, .run-analysis, " +
            "[data-action='run-analysis'], " +
            "[data-action='analyze']"
        );


    /*
       If the HTML does not have a specific ID/class,
       first try to find the button near the textarea.
    */

    if (!runButton && situationInput) {

        /*
           First try the closest form.
        */

        const form =
            situationInput.closest("form");

        if (form) {

            const formButtons =
                form.querySelectorAll("button");

            if (formButtons.length > 0) {

                runButton =
                    Array.from(formButtons).find((button) => {

                        const text =
                            button.textContent
                                .trim()
                                .toLowerCase();

                        return (
                            text === "→" ||
                            text === "➜" ||
                            text.includes("run") ||
                            text.includes("analyze") ||
                            text.includes("analysis")
                        );

                    }) || formButtons[formButtons.length - 1];
            }
        }


        /*
           Try the nearest common analyst containers.
        */

        if (!runButton) {

            const container =
                situationInput.closest(
                    ".analysis-input, " +
                    ".analyst-input, " +
                    ".input-group, " +
                    ".analysis-form, " +
                    ".analyst-form, " +
                    ".analysis-query, " +
                    ".query-form, " +
                    ".analyst-section, " +
                    ".analyst-panel, " +
                    "section, " +
                    ".container"
                );

            if (container) {

                const buttons =
                    container.querySelectorAll("button");

                if (buttons.length > 0) {

                    runButton =
                        Array.from(buttons).find((button) => {

                            const text =
                                button.textContent
                                    .trim()
                                    .toLowerCase();

                            return (
                                text === "→" ||
                                text === "➜" ||
                                text === "➝" ||
                                text === "⟶" ||
                                text.includes("run ai analysis") ||
                                text.includes("run analysis") ||
                                text.includes("analyze") ||
                                text.includes("analysis") ||
                                text.includes("submit")
                            );

                        }) || buttons[buttons.length - 1];
                }
            }
        }
    }


    /*
       Final fallback.

       The live FireGuard analyst interface currently
       displays a simple white arrow button.

       Search every button on the page.
    */

    if (!runButton) {

        const allButtons =
            document.querySelectorAll("button");

        runButton =
            Array.from(allButtons).find((button) => {

                const text =
                    button.textContent
                        .trim()
                        .toLowerCase();

                const ariaLabel =
                    (
                        button.getAttribute("aria-label") ||
                        ""
                    )
                    .trim()
                    .toLowerCase();

                const title =
                    (
                        button.getAttribute("title") ||
                        ""
                    )
                    .trim()
                    .toLowerCase();

                return (
                    text === "→" ||
                    text === "➜" ||
                    text === "➝" ||
                    text === "⟶" ||
                    text.includes("run ai analysis") ||
                    text.includes("run analysis") ||
                    text.includes("analyze") ||
                    text.includes("analysis") ||
                    text.includes("submit") ||
                    ariaLabel.includes("analyze") ||
                    ariaLabel.includes("analysis") ||
                    ariaLabel.includes("run") ||
                    title.includes("analyze") ||
                    title.includes("analysis") ||
                    title.includes("run")
                );

            }) || null;
    }


    /*
       Last-resort fallback:
       If there is exactly one button on the analyst
       page and we have an input, use that button.
    */

    if (!runButton && situationInput) {

        const pageButtons =
            document.querySelectorAll("button");

        if (pageButtons.length === 1) {

            runButton =
                pageButtons[0];
        }
    }


    /* =====================================================
       ANALYSIS OUTPUT
    ===================================================== */

    /*
       Locate the right-hand intelligence panel.
       We support several possible class/id names so
       this works with your current analyst.html.
    */

    let analysisOutput =
        document.querySelector(
            "#analysisOutput, " +
            "#analysis-result, " +
            ".analysis-output, " +
            ".analysis-result, " +
            ".engine-panel"
        );


    /*
       If there is no dedicated output element, look for
       the large right-side panel.
    */

    if (!analysisOutput) {

        const panels =
            document.querySelectorAll(
                ".panel, .card, .analysis-panel"
            );

        if (panels.length > 1) {
            analysisOutput = panels[panels.length - 1];
        }
    }


    /* =====================================================
       FIND QUICK ANALYSIS BUTTONS
    ===================================================== */

    const quickButtons =
        document.querySelectorAll(
            ".quick-analysis button, " +
            ".quick-card, " +
            ".quick-analysis-item, " +
            "[data-analysis]"
        );


    /* =====================================================
       ANALYSIS DATA
    ===================================================== */

    const getFormData = () => {

        const situation =
            situationInput
                ? situationInput.value.trim()
                : "";

        const region =
            regionInput
                ? regionInput.value
                : "Chennai";

        const mode =
            modeInput
                ? modeInput.value
                : "Thermal Anomaly Analysis";

        return {
            situation,
            region,
            mode
        };
    };


    /* =====================================================
       LOADING STATE
    ===================================================== */

    const showLoading = () => {

        if (!analysisOutput) return;

        analysisOutput.innerHTML = `
            <div class="analysis-loading"
                 style="
                    min-height:420px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    flex-direction:column;
                    text-align:center;
                    padding:40px;
                 ">

                <div style="
                    width:48px;
                    height:48px;
                    border:3px solid rgba(255,69,45,.2);
                    border-top-color:#ff452d;
                    border-radius:50%;
                    animation:fireguardSpin 1s linear infinite;
                    margin-bottom:25px;
                 "></div>

                <div style="
                    font-size:18px;
                    letter-spacing:3px;
                    text-transform:uppercase;
                    color:#ffffff;
                    margin-bottom:12px;
                 ">
                    FireGuard Intelligence Engine
                </div>

                <div style="
                    color:#777;
                    font-size:14px;
                 ">
                    Analyzing thermal and regional signals...
                </div>

            </div>
        `;

        addSpinnerAnimation();
    };


    /* =====================================================
       SPINNER CSS
    ===================================================== */

    const addSpinnerAnimation = () => {

        if (document.getElementById("fireguard-spinner-style")) {
            return;
        }

        const style =
            document.createElement("style");

        style.id =
            "fireguard-spinner-style";

        style.textContent = `
            @keyframes fireguardSpin {
                from {
                    transform: rotate(0deg);
                }

                to {
                    transform: rotate(360deg);
                }
            }
        `;

        document.head.appendChild(style);
    };


    /* =====================================================
       ESCAPE HTML
    ===================================================== */

    const escapeHTML = (value) => {

        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    };


    /* =====================================================
       RISK COLOR
    ===================================================== */

    const getRiskColor = (level) => {

        const value =
            String(level || "").toUpperCase();

        if (value === "CRITICAL") {
            return "#ff3828";
        }

        if (value === "HIGH") {
            return "#ff7614";
        }

        if (value === "MODERATE") {
            return "#ffd000";
        }

        if (value === "LOW") {
            return "#20e875";
        }

        return "#ff452d";
    };


    /* =====================================================
       DISPLAY ANALYSIS
    ===================================================== */

    const displayAnalysis = (data) => {

        if (!analysisOutput) {

            console.error(
                "FireGuard: analysis output panel not found."
            );

            return;
        }


        const threat =
            data.threat_level ||
            data.threat ||
            "UNKNOWN";


        const score =
            data.score ??
            data.risk_score ??
            0;


        const thermal =
            data.thermal_signal ||
            data.temperature ||
            "N/A";


        const industrial =
            data.industrial_proximity ||
            data.industrial_risk ||
            "N/A";


        const population =
            data.population_exposure ||
            data.population_risk ||
            "N/A";


        const confidence =
            data.ai_confidence ||
            data.confidence ||
            "N/A";


        let explanation =
            data.explanation ||
            "No explanation was returned by the intelligence engine.";


        /*
           Flask may return explanation as an array.
        */

        if (Array.isArray(explanation)) {

            explanation =
                explanation.join(" ");
        }


        let recommendations =
            data.recommended_response ||
            data.recommendations ||
            [];


        if (!Array.isArray(recommendations)) {

            recommendations =
                [recommendations];
        }


        const riskColor =
            getRiskColor(threat);


        const recommendationHTML =
            recommendations
                .filter(Boolean)
                .map((item) => {

                    return `
                        <li>
                            ${escapeHTML(item)}
                        </li>
                    `;
                })
                .join("");


        analysisOutput.innerHTML = `

            <div class="fireguard-analysis-result">

                <!-- ENGINE HEADER -->

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    border-bottom:1px solid #252525;
                    padding:22px 26px;
                    margin-bottom:26px;
                ">

                    <div style="
                        display:flex;
                        align-items:center;
                        gap:12px;
                    ">

                        <span style="
                            width:14px;
                            height:14px;
                            border-radius:50%;
                            background:${riskColor};
                            box-shadow:
                                0 0 18px ${riskColor};
                            display:inline-block;
                        "></span>

                        <span style="
                            letter-spacing:2px;
                            font-size:13px;
                            color:#c8c8c8;
                            text-transform:uppercase;
                        ">
                            FireGuard Intelligence Engine
                        </span>

                    </div>

                    <span style="
                        color:#888;
                        font-size:12px;
                        text-transform:uppercase;
                    ">
                        Analysis Complete
                    </span>

                </div>


                <!-- THREAT LEVEL -->

                <div style="
                    margin:0 26px 18px;
                    border:1px solid rgba(255,69,45,.35);
                    background:rgba(70,10,5,.18);
                    padding:28px;
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div>

                        <div style="
                            color:#777;
                            font-size:10px;
                            letter-spacing:4px;
                            margin-bottom:10px;
                            text-transform:uppercase;
                        ">
                            AI Assessed Threat Level
                        </div>

                        <div style="
                            color:${riskColor};
                            font-size:34px;
                            font-weight:800;
                        ">
                            ${escapeHTML(threat)}
                        </div>

                    </div>

                    <div style="
                        font-size:42px;
                        font-weight:800;
                        color:#f5f5f5;
                    ">
                        ${escapeHTML(score)}
                        <span style="
                            font-size:14px;
                            color:#777;
                            font-weight:400;
                        ">
                            /100
                        </span>
                    </div>

                </div>


                <!-- METRICS -->

                <div style="
                    display:grid;
                    grid-template-columns:
                        repeat(2,minmax(0,1fr));
                    gap:14px;
                    padding:0 26px;
                ">


                    <!-- THERMAL -->

                    <div style="
                        border:1px solid #252525;
                        padding:24px;
                        background:#0b0b0b;
                    ">

                        <div style="
                            color:#777;
                            font-size:10px;
                            letter-spacing:3px;
                            text-transform:uppercase;
                            margin-bottom:10px;
                        ">
                            Thermal Signal
                        </div>

                        <div style="
                            color:#fff;
                            font-size:24px;
                            font-weight:700;
                            margin-bottom:8px;
                        ">
                            ${escapeHTML(thermal)}
                        </div>

                        <div style="
                            color:#777;
                            font-size:13px;
                            line-height:1.6;
                        ">
                            Persistent thermal signature
                            detected across observations.
                        </div>

                    </div>


                    <!-- INDUSTRIAL -->

                    <div style="
                        border:1px solid #252525;
                        padding:24px;
                        background:#0b0b0b;
                    ">

                        <div style="
                            color:#777;
                            font-size:10px;
                            letter-spacing:3px;
                            text-transform:uppercase;
                            margin-bottom:10px;
                        ">
                            Industrial Proximity
                        </div>

                        <div style="
                            color:#fff;
                            font-size:24px;
                            font-weight:700;
                            margin-bottom:8px;
                        ">
                            ${escapeHTML(industrial)}
                        </div>

                        <div style="
                            color:#777;
                            font-size:13px;
                            line-height:1.6;
                        ">
                            Potential exposure to industrial
                            infrastructure.
                        </div>

                    </div>


                    <!-- POPULATION -->

                    <div style="
                        border:1px solid #252525;
                        padding:24px;
                        background:#0b0b0b;
                    ">

                        <div style="
                            color:#777;
                            font-size:10px;
                            letter-spacing:3px;
                            text-transform:uppercase;
                            margin-bottom:10px;
                        ">
                            Population Exposure
                        </div>

                        <div style="
                            color:#fff;
                            font-size:24px;
                            font-weight:700;
                            margin-bottom:8px;
                        ">
                            ${escapeHTML(population)}
                        </div>

                        <div style="
                            color:#777;
                            font-size:13px;
                            line-height:1.6;
                        ">
                            Nearby populated areas may
                            increase consequence severity.
                        </div>

                    </div>


                    <!-- CONFIDENCE -->

                    <div style="
                        border:1px solid #252525;
                        padding:24px;
                        background:#0b0b0b;
                    ">

                        <div style="
                            color:#777;
                            font-size:10px;
                            letter-spacing:3px;
                            text-transform:uppercase;
                            margin-bottom:10px;
                        ">
                            AI Confidence
                        </div>

                        <div style="
                            color:#fff;
                            font-size:24px;
                            font-weight:700;
                            margin-bottom:8px;
                        ">
                            ${escapeHTML(confidence)}
                        </div>

                        <div style="
                            color:#777;
                            font-size:13px;
                            line-height:1.6;
                        ">
                            Confidence based on the available
                            simulated signals.
                        </div>

                    </div>

                </div>


                <!-- EXPLANATION -->

                <div style="
                    margin:18px 26px 0;
                    border:1px solid #252525;
                    padding:26px;
                    background:#0b0b0b;
                ">

                    <div style="
                        color:#ff7614;
                        font-size:10px;
                        letter-spacing:4px;
                        text-transform:uppercase;
                        margin-bottom:16px;
                        font-weight:700;
                    ">
                        AI Explanation
                    </div>

                    <div style="
                        color:#bdbdbd;
                        font-size:15px;
                        line-height:1.8;
                    ">
                        ${escapeHTML(explanation)}
                    </div>

                </div>


                <!-- RECOMMENDED RESPONSE -->

                <div style="
                    margin:18px 26px 28px;
                    border:1px solid rgba(255,69,45,.3);
                    background:rgba(70,10,5,.16);
                    padding:26px;
                ">

                    <div style="
                        color:#ff7614;
                        font-size:10px;
                        letter-spacing:4px;
                        text-transform:uppercase;
                        margin-bottom:16px;
                        font-weight:700;
                    ">
                        Recommended Response
                    </div>

                    <ul style="
                        margin:0;
                        padding-left:20px;
                        color:#bdbdbd;
                        line-height:2;
                        font-size:14px;
                    ">
                        ${recommendationHTML}
                    </ul>

                </div>

            </div>
        `;
    };


    /* =====================================================
       ERROR DISPLAY
    ===================================================== */

    const displayError = (message) => {

        if (!analysisOutput) return;

        analysisOutput.innerHTML = `

            <div style="
                min-height:420px;
                display:flex;
                justify-content:center;
                align-items:center;
                flex-direction:column;
                text-align:center;
                padding:40px;
            ">

                <div style="
                    color:#ff3828;
                    font-size:24px;
                    font-weight:700;
                    margin-bottom:15px;
                ">
                    Analysis Error
                </div>

                <div style="
                    color:#888;
                    max-width:600px;
                    line-height:1.7;
                    margin-bottom:20px;
                ">
                    ${escapeHTML(message)}
                </div>

                <button
                    onclick="location.reload()"
                    style="
                        background:#ff3828;
                        color:#fff;
                        border:0;
                        padding:13px 24px;
                        cursor:pointer;
                        font-weight:700;
                        letter-spacing:1px;
                    "
                >
                    TRY AGAIN
                </button>

            </div>
        `;
    };


    /* =====================================================
       RUN AI ANALYSIS
    ===================================================== */

    const runAnalysis = async () => {

        const formData = getFormData();


        /* -----------------------------------------------
           Validate
        ----------------------------------------------- */

        if (!formData.situation) {

            alert(
                "Please describe the situation before running the analysis."
            );

            if (situationInput) {
                situationInput.focus();
            }

            return;
        }


        /* -----------------------------------------------
           Loading
        ----------------------------------------------- */

        showLoading();


        if (runButton) {

            runButton.disabled = true;

            runButton.dataset.originalText =
                runButton.innerHTML;

            runButton.innerHTML =
                "ANALYZING...";
        }


        try {

            console.log(
                "🔥 Sending FireGuard analysis:",
                formData
            );


            /* -------------------------------------------
               API REQUEST
            ------------------------------------------- */

            const response =
                await fetch(
                    `${API_BASE}/api/analyze`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(formData)
                    }
                );


            console.log(
                "FireGuard API status:",
                response.status
            );


            /* -------------------------------------------
               HTTP ERROR
            ------------------------------------------- */

            if (!response.ok) {

                let errorText =
                    `Server returned HTTP ${response.status}`;

                try {

                    const errorData =
                        await response.json();

                    if (errorData.error) {
                        errorText =
                            errorData.error;
                    }

                    if (errorData.message) {
                        errorText =
                            errorData.message;
                    }

                } catch (ignore) {}

                throw new Error(errorText);
            }


            /* -------------------------------------------
               JSON RESPONSE
            ------------------------------------------- */

            const data =
                await response.json();


            console.log(
                "🔥 FireGuard API response:",
                data
            );


            /*
               Some Flask APIs return:

               {
                   "result": {
                       ...
                   }
               }

               Others return the analysis directly.

               Support both.
            */

            const result =
                data.result ||
                data.analysis ||
                data;


            displayAnalysis(result);


        } catch (error) {

            console.error(
                "FireGuard analysis failed:",
                error
            );


            displayError(
                `Unable to complete the analysis. ${error.message}`
            );


        } finally {

            if (runButton) {

                runButton.disabled = false;

                runButton.innerHTML =
                    runButton.dataset.originalText ||
                    "RUN AI ANALYSIS →";
            }
        }
    };


    /* =====================================================
       RUN BUTTON EVENT
    ===================================================== */

    if (runButton) {

        runButton.addEventListener(
            "click",
            (event) => {

                event.preventDefault();

                runAnalysis();
            }
        );

        console.log(
            "🔥 FireGuard AI Analyst button connected."
        );

    } else {

        console.warn(
            "FireGuard: Run AI Analysis button not found."
        );
    }


    /* =====================================================
       QUICK ANALYSIS
    ===================================================== */

    quickButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const text =
                button.textContent
                    .trim()
                    .replace(/^🔥\s*/, "")
                    .replace(/^🏭\s*/, "")
                    .replace(/^👥\s*/, "")
                    .replace(/^🚨\s*/, "");


            if (!situationInput) {
                return;
            }


            /*
               Match the quick-analysis buttons
               from your current analyst interface.
            */

            const lower =
                text.toLowerCase();


            if (
                lower.includes("critical thermal") ||
                lower.includes("thermal anomaly")
            ) {

                situationInput.value =
                    "Analyze a critical thermal anomaly detected near an industrial area.";

            } else if (
                lower.includes("industrial")
            ) {

                situationInput.value =
                    "Assess the potential fire risk of a thermal anomaly near industrial infrastructure.";

            } else if (
                lower.includes("population")
            ) {

                situationInput.value =
                    "Estimate the potential population exposure around the detected thermal event.";

            } else if (
                lower.includes("emergency")
            ) {

                situationInput.value =
                    "Recommend an emergency response strategy for a high-risk thermal event.";
            }


            /*
               Automatically change the analysis mode
               when possible.
            */

            if (modeInput) {

                if (lower.includes("industrial")) {

                    selectMode(
                        modeInput,
                        "Fire Risk Assessment"
                    );

                } else if (
                    lower.includes("population")
                ) {

                    selectMode(
                        modeInput,
                        "Population Exposure"
                    );

                } else if (
                    lower.includes("emergency")
                ) {

                    selectMode(
                        modeInput,
                        "Emergency Response"
                    );

                } else {

                    selectMode(
                        modeInput,
                        "Thermal Anomaly Analysis"
                    );
                }
            }


            runAnalysis();
        });
    });


    /* =====================================================
       SELECT MODE HELPER
    ===================================================== */

    function selectMode(select, desiredText) {

        const options =
            Array.from(select.options || []);

        const match =
            options.find((option) =>
                option.text
                    .trim()
                    .toLowerCase()
                    .includes(
                        desiredText
                            .toLowerCase()
                    )
            );


        if (match) {

            select.value =
                match.value;

        } else {

            /*
               Fallback: select by partial value.
            */

            const valueMatch =
                options.find((option) =>
                    String(option.value)
                        .toLowerCase()
                        .includes(
                            desiredText
                                .toLowerCase()
                        )
                );

            if (valueMatch) {
                select.value =
                    valueMatch.value;
            }
        }
    }


    /* =====================================================
       KEYBOARD SHORTCUT
    ===================================================== */

    if (situationInput) {

        situationInput.addEventListener(
            "keydown",
            (event) => {

                /*
                   Ctrl + Enter = Run analysis
                */

                if (
                    event.ctrlKey &&
                    event.key === "Enter"
                ) {

                    event.preventDefault();

                    runAnalysis();
                }
            }
        );
    }


    /* =====================================================
       ANALYST PAGE READY
    ===================================================== */

    if (
        situationInput ||
        runButton ||
        analysisOutput
    ) {

        console.log(
            "🔥 FireGuard AI Analyst ready."
        );

        console.log(
            "Backend:",
            API_BASE
        );

        console.log(
            "Analysis button:",
            runButton
                ? "CONNECTED"
                : "NOT FOUND"
        );
    }

});