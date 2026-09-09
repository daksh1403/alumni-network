const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// Icon imports
const {
  FaDatabase, FaProjectDiagram, FaSitemap, FaTable, FaCubes,
  FaPuzzlePiece, FaLayerGroup, FaExchangeAlt, FaBalanceScale,
  FaCheckCircle, FaExclamationTriangle, FaKey, FaShieldAlt,
  FaBuilding, FaGraduationCap, FaUsers, FaLightbulb,
  FaArrowRight, FaNetworkWired, FaLock, FaLink,
  FaThList, FaStar, FaCodeBranch
} = require("react-icons/fa");

// ===================== ICON HELPERS =====================
function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// ===================== SETUP =====================
const prs = new pptxgen();
prs.defineLayout({ name: "WIDE", width: 13.33, height: 7.5 });
prs.layout = "WIDE";
prs.author = "Sagarika Kaistha, Praveen G, Daksh Agarwal";
prs.title = "Alumni Network and Engagement Platform";

// Berry & Cream palette — distinctive for a DBMS project
const C = {
  primary: "5B2C6F",      // Deep plum
  secondary: "8E44AD",    // Purple
  accent: "D4A843",       // Gold
  light: "FDF6EC",        // Warm cream
  white: "FFFFFF",
  dark: "1A0E26",         // Near-black plum
  text: "2C1810",         // Dark brown
  muted: "7D6B7D",        // Muted mauve
  success: "27AE60",      // Emerald
  card: "FFFFFF",
  cardBorder: "E8D5E8",   // Light plum
  headerBg: "F5EEF8",     // Very light purple
};

const headerFont = "Georgia";
const bodyFont = "Calibri";

const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.10 });
const makeCardShadow = () => ({ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.12 });

// Slide counter for numbering
let slideNum = 0;
function num() { return String(++slideNum); }

// ===================== SLIDE FUNCTIONS =====================

function titleSlide(title, subtitle, members) {
  const s = prs.addSlide();
  s.background = { color: C.dark };

  // Large decorative circles
  s.addShape("ellipse", { x: -1.5, y: -1.5, w: 5, h: 5, fill: { color: C.primary, transparency: 40 } });
  s.addShape("ellipse", { x: 10, y: 4.5, w: 5, h: 5, fill: { color: C.secondary, transparency: 35 } });
  s.addShape("ellipse", { x: 8, y: -2, w: 3, h: 3, fill: { color: C.accent, transparency: 60 } });

  // Institution
  s.addText("Vellore Institute of Technology", {
    x: 1.2, y: 1.0, w: 8, h: 0.5, fontSize: 15, fontFace: bodyFont,
    color: C.accent, bold: true, margin: 0
  });
  s.addText("School of Computer Science and Engineering", {
    x: 1.2, y: 1.45, w: 8, h: 0.35, fontSize: 11, fontFace: bodyFont,
    color: C.muted, margin: 0
  });

  // Title
  s.addText(title, {
    x: 1.2, y: 2.3, w: 9, h: 1.6, fontSize: 40, fontFace: headerFont,
    color: C.white, bold: true, margin: 0
  });

  // Accent bar under title
  s.addShape("rect", { x: 1.2, y: 4.0, w: 2.5, h: 0.06, fill: { color: C.accent } });

  // Subtitle
  s.addText(subtitle, {
    x: 1.2, y: 4.3, w: 8, h: 0.5, fontSize: 16, fontFace: bodyFont,
    color: C.muted, margin: 0
  });

  // Course
  s.addText("Database Management Systems (CSE2005)  |  DA1", {
    x: 1.2, y: 5.0, w: 8, h: 0.3, fontSize: 11, fontFace: bodyFont,
    color: C.muted, margin: 0
  });

  // Team card
  s.addShape("rect", {
    x: 1.2, y: 5.6, w: 5.5, h: 1.3, fill: { color: C.primary, transparency: 40 },
    shadow: makeShadow()
  });
  s.addText("TEAM MEMBERS", {
    x: 1.45, y: 5.65, w: 5, h: 0.3, fontSize: 9, fontFace: bodyFont,
    color: C.accent, bold: true, charSpacing: 3, margin: 0
  });
  members.forEach((m, i) => {
    s.addText(m, {
      x: 1.45, y: 5.98 + i * 0.27, w: 5, h: 0.25, fontSize: 12,
      fontFace: bodyFont, color: C.white, margin: 0
    });
  });
}

function sectionSlide(title, subtitle) {
  const s = prs.addSlide();
  s.background = { color: C.dark };

  // Decorative elements
  s.addShape("ellipse", { x: -1, y: -1, w: 4, h: 4, fill: { color: C.primary, transparency: 40 } });
  s.addShape("ellipse", { x: 10.5, y: 5, w: 4, h: 4, fill: { color: C.secondary, transparency: 35 } });
  s.addShape("ellipse", { x: 11, y: -1.5, w: 2.5, h: 2.5, fill: { color: C.accent, transparency: 65 } });

  // Accent bar
  s.addShape("rect", { x: 5.5, y: 2.8, w: 2.33, h: 0.06, fill: { color: C.accent } });

  // Title
  s.addText(title, {
    x: 1.5, y: 3.0, w: 10.33, h: 1.2, fontSize: 38, fontFace: headerFont,
    color: C.white, bold: true, align: "center", margin: 0
  });

  // Subtitle
  s.addText(subtitle, {
    x: 1.5, y: 4.3, w: 10.33, h: 0.6, fontSize: 16, fontFace: bodyFont,
    color: C.muted, align: "center", margin: 0
  });
}

function addSlideNum(s) {
  s.addText(num(), { x: 12.5, y: 7.0, w: 0.6, h: 0.3, fontSize: 9, fontFace: bodyFont, color: C.muted, align: "right", margin: 0 });
}

function headerBar(s, title) {
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.95, fill: { color: C.primary } });
  s.addText(title, {
    x: 0.8, y: 0.18, w: 11, h: 0.6, fontSize: 24, fontFace: headerFont,
    color: C.white, bold: true, margin: 0
  });
}

// --- OVERVIEW SLIDE: Icon + text rows ---
function iconOverviewSlide(title, items) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const startY = 1.4;
  const rowH = 1.3;
  const iconSize = 0.55;

  items.forEach((item, i) => {
    const y = startY + i * rowH;

    // Icon circle
    s.addShape("ellipse", {
      x: 0.8, y: y + 0.1, w: 0.8, h: 0.8,
      fill: { color: item.iconBg || C.secondary }
    });
    s.addImage({
      data: item.icon, x: 0.8 + 0.4 - iconSize / 2, y: y + 0.1 + 0.4 - iconSize / 2,
      w: iconSize, h: iconSize
    });

    // Text
    s.addText(item.heading, {
      x: 2.0, y: y + 0.05, w: 10, h: 0.35, fontSize: 16, fontFace: bodyFont,
      color: C.primary, bold: true, margin: 0
    });
    s.addText(item.desc, {
      x: 2.0, y: y + 0.4, w: 10, h: 0.5, fontSize: 12, fontFace: bodyFont,
      color: C.muted, margin: 0
    });
  });

  addSlideNum(s);
}

// --- STAT CALLOUT SLIDE: Big numbers ---
function statCalloutSlide(title, stats) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const cols = stats.length;
  const totalW = 12;
  const gap = 0.4;
  const cardW = (totalW - (cols - 1) * gap) / cols;
  const startX = 0.67;

  stats.forEach((st, i) => {
    const x = startX + i * (cardW + gap);

    // Card bg
    s.addShape("rect", {
      x, y: 1.5, w: cardW, h: 4.8, fill: { color: C.white },
      shadow: makeCardShadow()
    });

    // Top accent
    s.addShape("rect", { x, y: 1.5, w: cardW, h: 0.08, fill: { color: st.accentColor || C.accent } });

    // Icon circle
    s.addShape("ellipse", {
      x: x + cardW / 2 - 0.45, y: 1.9, w: 0.9, h: 0.9,
      fill: { color: st.iconBg || C.primary }
    });
    s.addImage({
      data: st.icon,
      x: x + cardW / 2 - 0.25, y: 2.1, w: 0.5, h: 0.5
    });

    // Title
    s.addText(st.title, {
      x: x + 0.15, y: 3.1, w: cardW - 0.3, h: 0.4, fontSize: 15,
      fontFace: bodyFont, color: C.primary, bold: true, align: "center", margin: 0
    });

    // Items
    const rows = st.items.map(item => ({
      text: item,
      options: { fontSize: 11, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 8 }, paraSpaceAfter: 5 }
    }));
    s.addText(rows, {
      x: x + 0.2, y: 3.6, w: cardW - 0.4, h: 2.5, valign: "top", margin: 0
    });
  });

  addSlideNum(s);
}

// --- TWO COLUMN SLIDE ---
function twoColumnSlide(title, leftTitle, leftItems, rightTitle, rightItems) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const colW = 5.8;

  // Left card
  s.addShape("rect", {
    x: 0.5, y: 1.4, w: colW, h: 5.3, fill: { color: C.white },
    shadow: makeCardShadow()
  });
  s.addShape("rect", { x: 0.5, y: 1.4, w: colW, h: 0.07, fill: { color: C.secondary } });

  // Left title with icon circle
  s.addShape("ellipse", { x: 0.8, y: 1.75, w: 0.55, h: 0.55, fill: { color: C.primary } });
  s.addText(leftTitle.charAt(0), {
    x: 0.8, y: 1.75, w: 0.55, h: 0.55, fontSize: 18, fontFace: headerFont,
    color: C.white, bold: true, align: "center", valign: "middle", margin: 0
  });
  s.addText(leftTitle, {
    x: 1.55, y: 1.8, w: colW - 1.3, h: 0.4, fontSize: 15, fontFace: bodyFont,
    color: C.primary, bold: true, margin: 0
  });

  const leftRows = leftItems.map(item => ({
    text: item,
    options: { fontSize: 12, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 10 }, paraSpaceAfter: 6 }
  }));
  s.addText(leftRows, {
    x: 0.9, y: 2.5, w: colW - 0.8, h: 3.8, valign: "top", margin: 0
  });

  // Right card
  const rightX = 7.03;
  s.addShape("rect", {
    x: rightX, y: 1.4, w: colW, h: 5.3, fill: { color: C.white },
    shadow: makeCardShadow()
  });
  s.addShape("rect", { x: rightX, y: 1.4, w: colW, h: 0.07, fill: { color: C.accent } });

  s.addShape("ellipse", { x: rightX + 0.3, y: 1.75, w: 0.55, h: 0.55, fill: { color: C.accent } });
  s.addText(rightTitle.charAt(0), {
    x: rightX + 0.3, y: 1.75, w: 0.55, h: 0.55, fontSize: 18, fontFace: headerFont,
    color: C.white, bold: true, align: "center", valign: "middle", margin: 0
  });
  s.addText(rightTitle, {
    x: rightX + 1.05, y: 1.8, w: colW - 1.3, h: 0.4, fontSize: 15, fontFace: bodyFont,
    color: C.primary, bold: true, margin: 0
  });

  const rightRows = rightItems.map(item => ({
    text: item,
    options: { fontSize: 12, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 10 }, paraSpaceAfter: 6 }
  }));
  s.addText(rightRows, {
    x: rightX + 0.6, y: 2.5, w: colW - 0.9, h: 3.8, valign: "top", margin: 0
  });

  addSlideNum(s);
}

// --- THREE COLUMN CARDS ---
function threeColSlide(title, cards) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const cols = 3;
  const gap = 0.35;
  const cardW = (12.33 - (cols - 1) * gap) / cols;
  const startX = 0.5;
  const cardH = 5.3;

  cards.forEach((card, i) => {
    const x = startX + i * (cardW + gap);

    s.addShape("rect", {
      x, y: 1.4, w: cardW, h: cardH, fill: { color: C.white },
      shadow: makeCardShadow()
    });

    // Top colored band
    s.addShape("rect", { x, y: 1.4, w: cardW, h: 0.55, fill: { color: card.bandColor || C.primary } });

    // Icon in band
    s.addImage({
      data: card.icon,
      x: x + cardW / 2 - 0.2, y: 1.47, w: 0.4, h: 0.4
    });

    // Card title
    s.addText(card.title, {
      x: x + 0.2, y: 2.15, w: cardW - 0.4, h: 0.4, fontSize: 14,
      fontFace: bodyFont, color: C.primary, bold: true, align: "center", margin: 0
    });

    // Items
    const rows = card.items.map(item => ({
      text: item,
      options: { fontSize: 11, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 8 }, paraSpaceAfter: 5 }
    }));
    s.addText(rows, {
      x: x + 0.25, y: 2.65, w: cardW - 0.5, h: cardH - 1.4, valign: "top", margin: 0
    });
  });

  addSlideNum(s);
}

// --- FOUR COLUMN CARDS ---
function fourColSlide(title, cards) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const cols = 4;
  const gap = 0.3;
  const startX = 0.5;
  const endX = 12.5;
  const cardW = (endX - startX - (cols - 1) * gap) / cols;
  const cardH = 5.2;

  cards.forEach((card, i) => {
    const x = startX + i * (cardW + gap);

    s.addShape("rect", {
      x, y: 1.4, w: cardW, h: cardH, fill: { color: C.white },
      shadow: makeCardShadow()
    });

    // Top accent bar
    s.addShape("rect", { x, y: 1.4, w: cardW, h: 0.06, fill: { color: card.accentColor || C.secondary } });

    // Icon circle
    s.addShape("ellipse", {
      x: x + cardW / 2 - 0.4, y: 1.8, w: 0.8, h: 0.8,
      fill: { color: card.iconBg || C.primary }
    });
    s.addImage({
      data: card.icon,
      x: x + cardW / 2 - 0.22, y: 1.98, w: 0.44, h: 0.44
    });

    // Card title
    s.addText(card.title, {
      x: x + 0.1, y: 2.85, w: cardW - 0.2, h: 0.35, fontSize: 13,
      fontFace: bodyFont, color: C.primary, bold: true, align: "center", margin: 0
    });

    // Items
    const rows = card.items.map(item => ({
      text: item,
      options: { fontSize: 10, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 6 }, paraSpaceAfter: 4 }
    }));
    s.addText(rows, {
      x: x + 0.15, y: 3.3, w: cardW - 0.3, h: cardH - 2.1, valign: "top", margin: 0
    });
  });

  addSlideNum(s);
}

// --- TABLE SLIDE ---
function tableSlide(title, headers, data, options = {}) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const rows = [
    headers.map(h => ({
      text: h,
      options: { fontSize: 11, fontFace: bodyFont, color: C.white, bold: true, align: "center", fill: { color: C.primary } }
    })),
    ...data.map((row, ri) => row.map((c, ci) => ({
      text: String(c),
      options: {
        fontSize: 10, fontFace: bodyFont, color: C.text,
        align: ci === 0 ? "left" : "center",
        fill: { color: ri % 2 === 0 ? C.white : C.headerBg }
      }
    })))
  ];

  const colW = options.colW || headers.map(() => 12 / headers.length);
  const tableY = options.y || 1.4;
  const maxH = options.maxH || 5.3;

  s.addTable(rows, {
    x: 0.5, y: tableY, w: 12.33,
    colW: colW,
    border: { pt: 0.5, color: C.cardBorder },
    rowH: 0.32,
    fill: { color: C.white },
    shadow: makeShadow(),
  });

  addSlideNum(s);
}

// --- CONTENT/BULLET SLIDE ---
function contentSlide(title, items) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  // Content card
  s.addShape("rect", {
    x: 0.5, y: 1.4, w: 12.33, h: 5.3, fill: { color: C.white },
    shadow: makeCardShadow()
  });

  const rows = items.map(item => ({
    text: item,
    options: { fontSize: 14, fontFace: bodyFont, color: C.text, bullet: { type: "bullet", indent: 12 }, paraSpaceAfter: 10 }
  }));
  s.addText(rows, { x: 1.0, y: 1.7, w: 11.33, h: 4.7, valign: "top", margin: 0 });

  addSlideNum(s);
}

// --- THANK YOU SLIDE ---
function thankYouSlide() {
  const s = prs.addSlide();
  s.background = { color: C.dark };

  // Decorative
  s.addShape("ellipse", { x: -1, y: -1, w: 4.5, h: 4.5, fill: { color: C.primary, transparency: 35 } });
  s.addShape("ellipse", { x: 9.5, y: 4, w: 5, h: 5, fill: { color: C.secondary, transparency: 40 } });
  s.addShape("ellipse", { x: 6, y: -2, w: 2.5, h: 2.5, fill: { color: C.accent, transparency: 60 } });

  // Accent bar
  s.addShape("rect", { x: 5.5, y: 2.0, w: 2.33, h: 0.06, fill: { color: C.accent } });

  s.addText("THANK YOU", {
    x: 1, y: 2.3, w: 11.33, h: 1.2, fontSize: 52, fontFace: headerFont,
    color: C.white, bold: true, align: "center", charSpacing: 6, margin: 0
  });

  s.addText("Questions & Discussion", {
    x: 1, y: 3.6, w: 11.33, h: 0.6, fontSize: 18, fontFace: bodyFont,
    color: C.muted, align: "center", margin: 0
  });

  // Team card
  s.addShape("rect", {
    x: 3, y: 4.8, w: 7.33, h: 1.6, fill: { color: C.primary, transparency: 45 },
    shadow: makeCardShadow()
  });

  const members = [
    "Sagarika Kaistha (25BCE5091)",
    "Praveen G (25BCE5092)",
    "Daksh Agarwal (25BCE5098)"
  ];
  members.forEach((m, i) => {
    s.addText(m, {
      x: 3.2, y: 4.95 + i * 0.35, w: 6.93, h: 0.3, fontSize: 13,
      fontFace: bodyFont, color: C.white, align: "center", margin: 0
    });
  });
}

// --- THREE COLUMN TABLE ---
function threeColTableSlide(title, headers, data) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const rows = [
    headers.map(h => ({
      text: h,
      options: { fontSize: 12, fontFace: bodyFont, color: C.white, bold: true, align: "center", fill: { color: C.primary } }
    })),
    ...data.map((row, ri) => row.map((c, ci) => ({
      text: String(c),
      options: {
        fontSize: 11, fontFace: bodyFont, color: C.text,
        align: ci === 0 ? "left" : "center",
        fill: { color: ri % 2 === 0 ? C.white : C.headerBg }
      }
    })))
  ];

  s.addTable(rows, {
    x: 0.5, y: 1.4, w: 12.33,
    colW: [4.5, 3.5, 4.33],
    border: { pt: 0.5, color: C.cardBorder },
    rowH: 0.38,
    fill: { color: C.white },
    shadow: makeShadow(),
  });

  addSlideNum(s);
}

// --- TABLE WITH DESCRIPTION (wide first col) ---
function wideTableSlide(title, headers, data, firstColW) {
  const s = prs.addSlide();
  s.background = { color: C.light };
  headerBar(s, title);

  const rows = [
    headers.map(h => ({
      text: h,
      options: { fontSize: 11, fontFace: bodyFont, color: C.white, bold: true, align: "center", fill: { color: C.primary } }
    })),
    ...data.map((row, ri) => row.map((c, ci) => ({
      text: String(c),
      options: {
        fontSize: 10, fontFace: bodyFont, color: C.text,
        align: ci === 0 ? "left" : "center",
        fill: { color: ri % 2 === 0 ? C.white : C.headerBg }
      }
    })))
  ];

  const colW = headers.map((_, i) => i === 0 ? firstColW : (12.33 - firstColW) / (headers.length - 1));

  s.addTable(rows, {
    x: 0.5, y: 1.4, w: 12.33,
    colW: colW,
    border: { pt: 0.5, color: C.cardBorder },
    rowH: 0.32,
    fill: { color: C.white },
    shadow: makeShadow(),
  });

  addSlideNum(s);
}

// ===================== BUILD PRESENTATION =====================
async function build() {
  // Pre-render all icons
  const icons = {};
  const iconMap = {
    database: [FaDatabase, C.white],
    diagram: [FaProjectDiagram, C.white],
    sitemap: [FaSitemap, C.white],
    table: [FaTable, C.white],
    cubes: [FaCubes, C.white],
    puzzle: [FaPuzzlePiece, C.white],
    layers: [FaLayerGroup, C.white],
    exchange: [FaExchangeAlt, C.white],
    balance: [FaBalanceScale, C.white],
    check: [FaCheckCircle, C.white],
    warning: [FaExclamationTriangle, C.white],
    key: [FaKey, C.white],
    shield: [FaShieldAlt, C.white],
    building: [FaBuilding, C.white],
    grad: [FaGraduationCap, C.white],
    users: [FaUsers, C.white],
    lightbulb: [FaLightbulb, C.white],
    arrow: [FaArrowRight, C.white],
    network: [FaNetworkWired, C.white],
    lock: [FaLock, C.white],
    link: [FaLink, C.white],
    list: [FaThList, C.white],
    star: [FaStar, C.white],
    branch: [FaCodeBranch, C.white],
    // Dark versions for light backgrounds
    databaseDark: [FaDatabase, C.primary],
    diagramDark: [FaProjectDiagram, C.primary],
    sitemapDark: [FaSitemap, C.primary],
    tableDark: [FaTable, C.primary],
    cubesDark: [FaCubes, C.primary],
    balanceDark: [FaBalanceScale, C.primary],
    keyDark: [FaKey, C.primary],
    shieldDark: [FaShieldAlt, C.primary],
    checkDark: [FaCheckCircle, "#27AE60"],
    warningDark: [FaExclamationTriangle, C.accent],
    gradDark: [FaGraduationCap, C.primary],
    usersDark: [FaUsers, C.secondary],
    buildingDark: [FaBuilding, C.primary],
    networkDark: [FaNetworkWired, C.secondary],
    lockDark: [FaLock, C.primary],
    linkDark: [FaLink, C.secondary],
    lightbulbDark: [FaLightbulb, C.accent],
    branchDark: [FaCodeBranch, C.secondary],
    starDark: [FaStar, C.accent],
    puzzleDark: [FaPuzzlePiece, C.secondary],
    layersDark: [FaLayerGroup, C.primary],
    exchangeDark: [FaExchangeAlt, C.secondary],
  };

  for (const [name, [comp, color]] of Object.entries(iconMap)) {
    icons[name] = await iconToBase64Png(comp, color);
  }

  // ===================== SLIDES =====================

  // 1. TITLE
  titleSlide(
    "ALUMNI NETWORK AND\nENGAGEMENT PLATFORM",
    "Database Management Systems Project  |  DA1",
    ["Sagarika Kaistha - 25BCE5091", "Praveen G - 25BCE5092", "Daksh Agarwal - 25BCE5098"]
  );

  // 2. OVERVIEW
  fourColSlide("What We Cover", [
    { icon: icons.diagram, iconBg: C.primary, accentColor: C.primary, title: "ER Model", items: ["Entities & Attributes", "Relationships", "Cardinality & Participation", "12 Strong Entities"] },
    { icon: icons.sitemap, iconBg: C.secondary, accentColor: C.secondary, title: "EER Model", items: ["Generalization Hierarchy", "ISA Relationship", "Aggregation", "5 Hierarchies"] },
    { icon: icons.balance, iconBg: "27AE60", accentColor: "27AE60", title: "Normalization", items: ["1NF through BCNF", "Functional Dependencies", "Decomposition", "18 Tables Normalized"] },
    { icon: icons.table, iconBg: C.accent, accentColor: C.accent, title: "Relational Schema", items: ["Tables & Keys", "Constraints", "Referential Integrity", "30 FK Relationships"] },
  ]);

  // 3. PROBLEM STATEMENT
  statCalloutSlide("Problem Statement", [
    {
      icon: icons.warning, iconBg: C.accent, accentColor: C.accent,
      title: "Challenges",
      items: [
        "No centralized alumni tracking system",
        "Lost connections after graduation",
        "Manual, error-prone donation tracking",
        "No structured mentorship platform",
        "Fragmented event management"
      ]
    },
    {
      icon: icons.lightbulb, iconBg: C.secondary, accentColor: C.secondary,
      title: "Our Approach",
      items: [
        "Complete relational database system",
        "Alumni information management",
        "Automated events & donations",
        "Built-in job & mentorship support",
        "Forum for ongoing engagement"
      ]
    },
    {
      icon: icons.database, iconBg: C.primary, accentColor: C.primary,
      title: "Deliverables",
      items: [
        "ER & EER model diagrams",
        "Normalization up to BCNF",
        "Complete relational schema",
        "30 foreign key relationships",
        "3 SQL views for reporting"
      ]
    }
  ]);

  // 4. SECTION: ER MODEL
  sectionSlide("ENTITY-RELATIONSHIP MODEL", "Entities, Attributes, and Relationships");

  // 5. TYPES OF ATTRIBUTES (icon rows)
  iconOverviewSlide("Types of Attributes", [
    { icon: icons.checkDark, iconBg: C.headerBg, heading: "Simple & Composite", desc: "FirstName, Email (atomic)  |  Address = City + State + PinCode" },
    { icon: icons.usersDark, iconBg: C.headerBg, heading: "Multi-valued & Derived", desc: "Skills, PhoneNumbers (multiple values)  |  Age (calculated from DOB)" },
    { icon: icons.keyDark, iconBg: C.headerBg, heading: "Key & NULL", desc: "PersonID (unique identifier)  |  LinkedInProfile (optional)" },
    { icon: icons.databaseDark, iconBg: C.headerBg, heading: "Stored & Single-valued", desc: "GraduationYear (directly stored)  |  Email (one value per entity)" },
  ]);

  // 6. STRONG ENTITIES
  tableSlide("Strong Entities",
    ["Entity", "Primary Key", "Key Attributes", "Type"],
    [
      ["ALUMNI", "AlumniID", "FirstName, LastName, Email, GraduationYear", "Strong"],
      ["DEPARTMENT", "DeptID", "DeptName, DeptCode, HODPersonID", "Strong"],
      ["BATCH", "BatchID", "BatchYear, DeptID, Section", "Strong"],
      ["COMPANY", "CompanyID", "CompanyName, Industry, SizeID", "Strong"],
      ["SKILL", "SkillID", "SkillName, SkillCategory", "Strong"],
      ["EVENT", "EventID", "EventName, EventTypeID, EventDate", "Strong"],
      ["DONATION", "DonationID", "Amount, DonationDate, PaymentMethod", "Strong"],
      ["JOB", "JobID", "JobTitle, CompanyID, JobType", "Strong"],
      ["MENTORSHIP", "MentorshipID", "MentorID, MenteeID, StartDate", "Weak"],
      ["FORUM", "ForumID", "ForumName, Category, CreatedBy", "Strong"],
      ["POST", "PostID", "ForumID, AuthorID, Title", "Strong"],
      ["COMMENT", "CommentID", "PostID, AuthorID, ParentCommentID", "Strong"],
    ]
  );

  // 7. RELATIONSHIPS (Core)
  tableSlide("Relationships \u2014 Core",
    ["Entities", "Relationship", "Card.", "Participation"],
    [
      ["ALUMNI - DEPARTMENT", "belongs_to", "N:1", "Total / Partial"],
      ["ALUMNI - BATCH", "belongs_to", "N:1", "Total / Partial"],
      ["ALUMNI - COMPANY", "works_at", "N:1", "Partial / Partial"],
      ["ALUMNI - SKILL", "has", "M:N", "Partial / Partial"],
      ["ALUMNI - EVENT", "attends", "M:N", "Partial / Partial"],
      ["ALUMNI - EVENT", "organizes", "1:N", "Partial / Partial"],
      ["ALUMNI - DONATION", "makes", "1:N", "Partial / Partial"],
      ["ALUMNI - JOB", "posts", "1:N", "Partial / Partial"],
      ["COMPANY - JOB", "offers", "1:N", "Partial / Partial"],
      ["ALUMNI - MENTORSHIP", "mentors (recursive)", "1:N", "Partial / Total"],
    ]
  );

  // 7b. RELATIONSHIPS (Content & Forum)
  tableSlide("Relationships \u2014 Content & Forum",
    ["Entities", "Relationship", "Card.", "Participation"],
    [
      ["ALUMNI - FORUM", "creates", "1:N", "Partial / Total"],
      ["FORUM - POST", "contains", "1:N", "Partial / Total"],
      ["ALUMNI - POST", "authors", "1:N", "Partial / Total"],
      ["POST - COMMENT", "has", "1:N", "Partial / Total"],
      ["ALUMNI - COMMENT", "writes", "1:N", "Partial / Total"],
      ["COMMENT - COMMENT", "replies_to (self-ref)", "1:N", "Partial / Partial"],
    ]
  );

  // 8. SECTION: EER
  sectionSlide("EXTENDED ER MODEL", "Generalization, Specialization & Aggregation");

  // 9. GENERALIZATION
  threeColSlide("Generalization / Specialization", [
    {
      icon: icons.users, bandColor: C.primary,
      title: "PERSON Hierarchy",
      items: [
        "PERSON supertype \u2192 ALUMNI, STUDENT, ADMIN",
        "Common: Name, Email, Phone, DOB, Gender",
        "Disjoint + Total: every person is exactly one subtype",
        "PersonID links supertype to subtypes"
      ]
    },
    {
      icon: icons.network, bandColor: C.secondary,
      title: "Other Hierarchies",
      items: [
        "CONTENT \u2192 POST, COMMENT, REPLY",
        "TRANSACTION \u2192 DONATION, EVENT_FEE, MEMBERSHIP",
        "EVENT \u2192 REUNION, WORKSHOP, SEMINAR, NETWORKING",
        "JOB \u2192 FULL_TIME, PART_TIME, INTERNSHIP"
      ]
    },
    {
      icon: icons.table, bandColor: C.accent,
      title: "Implementation",
      items: [
        "Supertype table for shared attributes",
        "Subtype tables with PK = FK to supertype",
        "ISA triangle in ER diagram",
        "Clean separation of concerns"
      ]
    }
  ]);

  // 10. PERSON HIERARCHY
  threeColTableSlide("PERSON Generalization Hierarchy",
    ["Entity", "Type", "Attributes"],
    [
      ["PERSON", "Supertype", "PersonID (PK), FirstName, LastName, Email, Phone, DOB, Gender, Address"],
      ["ALUMNI", "Subtype", "PersonID (PK,FK), GraduationYear, DeptID, BatchID, CurrentCompanyID, CurrentPosition, LinkedIn, IsActive"],
      ["STUDENT", "Subtype", "PersonID (PK,FK), StudentID, EnrollmentYear, DeptID, CurrentSemester, CGPA"],
    ]
  );

  // 11. AGGREGATION
  statCalloutSlide("Aggregation \u2014 MENTORSHIP", [
    {
      icon: icons.puzzle, iconBg: C.accent, accentColor: C.accent,
      title: "The Problem",
      items: [
        "Mentorship relates two ALUMNI entities",
        "But it carries its own attributes",
        "Cannot store without aggregation",
        "Standard ER cannot express this"
      ]
    },
    {
      icon: icons.lightbulb, iconBg: C.secondary, accentColor: C.secondary,
      title: "The Solution",
      items: [
        "Treat mentorship as higher-level entity",
        "MentorshipID as Primary Key",
        "MentorID & MenteeID as Foreign Keys",
        "Own relationship attributes preserved"
      ]
    },
    {
      icon: icons.star, iconBg: C.primary, accentColor: C.primary,
      title: "Key Attributes",
      items: [
        "StartDate, EndDate",
        "Status: Active / Completed / Paused",
        "AreaID (FK to MENTORSHIP_AREA)",
        "Goals, Feedback, Rating"
      ]
    }
  ]);

  // 12. SECTION: NORMALIZATION
  sectionSlide("NORMALIZATION", "Eliminating Redundancy & Preventing Anomalies");

  // 13. WHY NORMALIZE
  twoColumnSlide("Why Normalize?",
    "Problems Without", [
      "DeptName change requires updating 100s of rows",
      "Cannot add a department without alumni data",
      "Deleting last alumni loses department info",
      "Data repeated everywhere wastes space",
      "Update anomalies corrupt consistency"
    ],
    "Benefits With", [
      "Each fact stored in exactly one place",
      "Changes propagate through foreign keys",
      "No update, insertion, or deletion anomalies",
      "Referential integrity enforced by DBMS",
      "Clean, predictable query performance"
    ]
  );

  // 14. 1NF
  twoColumnSlide("First Normal Form (1NF)",
    "The Rule", [
      "All attribute values must be atomic",
      "No multi-valued attributes in a column",
      "No repeating groups or nested tables",
      "Each row-column intersection has one value"
    ],
    "Our Fixes", [
      "Skills \u2192 ALUMNI_SKILL junction table",
      "Events \u2192 EVENT_REGISTRATION junction table",
      "Address \u2192 decomposed to City, State, PinCode",
      "Clean atomic values throughout"
    ]
  );

  // 15. 2NF AND 3NF
  twoColumnSlide("2NF and 3NF",
    "2NF \u2014 No Partial Dependencies", [
      "All tables have a single-column primary key",
      "No non-prime attribute depends on part of a key",
        "Automatically satisfied in our design",
      "Every determinant is the full key"
    ],
    "3NF \u2014 No Transitive Dependencies", [
      "DeptName depended on DeptID, not the PK \u2192 fixed",
      "Separated DEPARTMENT as its own table",
      "HODName \u2192 HODPersonID FK (removed transitive dep)",
      "EventType \u2192 EVENT_TYPE lookup table"
    ]
  );

  // 16. BCNF
  statCalloutSlide("BCNF and Beyond", [
    {
      icon: icons.check, iconBg: "27AE60", accentColor: "27AE60",
      title: "BCNF",
      items: [
        "Every determinant must be a candidate key",
        "Stricter than 3NF",
        "All 15 core tables satisfy BCNF",
        "No remaining anomalies"
      ]
    },
    {
      icon: icons.layers, iconBg: C.secondary, accentColor: C.secondary,
      title: "4NF Verification",
      items: [
        "No multi-valued dependencies",
        "Multi-valued attrs decomposed to junction tables",
        "ALUMNI_SKILL, EVENT_REGISTRATION, JOB_APPLICATION",
        "Clean M:N resolution"
      ]
    },
    {
      icon: icons.star, iconBg: C.primary, accentColor: C.primary,
      title: "5NF Verification",
      items: [
        "All join dependencies implied by candidate keys",
        "No further lossless decomposition possible",
        "Result: 20 fully normalized tables",
        "Ready for production use"
      ]
    }
  ]);

  // 17. NORMALIZATION SUMMARY
  tableSlide("Normalization Summary (V2)",
    ["Table", "1NF", "2NF", "3NF", "BCNF", "V2 Change"],
    [
      ["ALUMNI", "\u2713", "\u2713", "\u2713", "\u2713", "Decomposed transitive deps"],
      ["DEPARTMENT", "\u2713", "\u2713", "\u2713", "\u2713", "HODName \u2192 HODPersonID FK"],
      ["BATCH", "\u2713", "\u2713", "\u2713", "\u2713", "Single attribute PK"],
      ["COMPANY", "\u2713", "\u2713", "\u2713", "\u2713", "CompanySize \u2192 SizeID FK"],
      ["SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "Single attribute PK"],
      ["EVENT", "\u2713", "\u2713", "\u2713", "\u2713", "EventType \u2192 EventTypeID FK"],
      ["DONATION", "\u2713", "\u2713", "\u2713", "\u2713", "Single attribute PK"],
      ["JOB", "\u2713", "\u2713", "\u2713", "\u2713", "Decomposed transitive deps"],
      ["MENTORSHIP", "\u2713", "\u2713", "\u2713", "\u2713", "MentorshipArea \u2192 AreaID FK"],
      ["FORUM", "\u2713", "\u2713", "\u2713", "\u2713", "Single attribute PK"],
      ["POST", "\u2713", "\u2713", "\u2713", "\u2713", "LikesCount denormalized"],
      ["COMMENT", "\u2713", "\u2713", "\u2713", "\u2713", "Self-referencing FK"],
      ["ALUMNI_SKILL", "\u2713", "\u2713", "\u2713", "\u2713", "Junction table"],
      ["EVENT_REGISTRATION", "\u2713", "\u2713", "\u2713", "\u2713", "Junction table"],
      ["JOB_APPLICATION", "\u2713", "\u2713", "\u2713", "\u2713", "New in V2"],
      ["ADMIN", "\u2713", "\u2713", "\u2713", "\u2713", "Subtype of PERSON"],
      ["PERSON", "\u2713", "\u2713", "\u2713", "\u2713", "Supertype"],
      ["STUDENT", "\u2713", "\u2713", "\u2713", "\u2713", "Subtype of PERSON"],
    ]
  );

  // 18. SECTION: RELATIONAL SCHEMA
  sectionSlide("RELATIONAL SCHEMA", "Tables, Constraints & Referential Integrity");

  // 19. CORE TABLES
  tableSlide("Core Tables",
    ["Table", "Primary Key", "Foreign Keys"],
    [
      ["PERSON", "PersonID", "\u2014"],
      ["ALUMNI", "PersonID", "PersonID, DeptID, BatchID, CurrentCompanyID"],
      ["STUDENT", "PersonID", "PersonID, DeptID"],
      ["ADMIN", "PersonID", "PersonID"],
      ["DEPARTMENT", "DeptID", "HODPersonID"],
      ["BATCH", "BatchID", "DeptID"],
      ["COMPANY", "CompanyID", "SizeID"],
      ["EVENT", "EventID", "EventTypeID, OrganizerID"],
      ["DONATION", "DonationID", "DonorID"],
      ["JOB", "JobID", "CompanyID, PostedBy"],
      ["MENTORSHIP", "MentorshipID", "MentorID, MenteeID, AreaID"],
      ["FORUM", "ForumID", "CreatedBy"],
      ["POST", "PostID", "ForumID, AuthorID"],
      ["COMMENT", "CommentID", "PostID, AuthorID, ParentCommentID"],
    ]
  );

  // 20. LOOKUP & JUNCTION TABLES
  tableSlide("Lookup & Junction Tables",
    ["Table", "Type", "Key Columns", "Purpose"],
    [
      ["EVENT_TYPE", "Lookup", "TypeID, TypeName", "Event categories"],
      ["COMPANY_SIZE", "Lookup", "SizeID, SizeRange", "Company sizes"],
      ["MENTORSHIP_AREA", "Lookup", "AreaID, AreaName", "Mentorship areas"],
      ["ALUMNI_SKILL", "Junction", "AlumniID, SkillID", "M:N skills resolver"],
      ["EVENT_REGISTRATION", "Junction", "AlumniID, EventID", "M:N event attendance"],
      ["JOB_APPLICATION", "Junction", "ApplicationID, JobID", "M:N job applications"],
    ]
  );

  // 21. CONSTRAINTS
  iconOverviewSlide("Constraints Applied", [
    { icon: icons.keyDark, iconBg: C.headerBg, heading: "Key Constraints", desc: "Primary Keys on all 20 tables | UNIQUE on Email, StudentID, TransactionID | CHECK for validation" },
    { icon: icons.linkDark, iconBg: C.headerBg, heading: "Referential Integrity", desc: "30 foreign key relationships with CASCADE, RESTRICT, and SET NULL actions" },
    { icon: icons.shieldDark, iconBg: C.headerBg, heading: "Domain Constraints", desc: "NOT NULL on required fields | Enumerated types for Status, Gender, PaymentMethod" },
    { icon: icons.databaseDark, iconBg: C.headerBg, heading: "SQL Views", desc: "AlumniProfileView | EventSummaryView | DonationSummaryView for common queries" },
  ]);

  // 22. CONCLUSION
  fourColSlide("Conclusion", [
    {
      icon: icons.diagram, iconBg: C.primary, accentColor: C.primary,
      title: "ER Model",
      items: [
        "All 8 attribute types demonstrated",
        "12 strong entities defined",
        "17 relationships with cardinality",
        "Full participation constraints"
      ]
    },
    {
      icon: icons.sitemap, iconBg: C.secondary, accentColor: C.secondary,
      title: "EER Model",
      items: [
        "5 generalization hierarchies",
        "PERSON/CONTENT/TRANSACTION/EVENT/JOB",
        "ISA with disjoint + total constraints",
        "Aggregation for MENTORSHIP"
      ]
    },
    {
      icon: icons.balance, iconBg: "27AE60", accentColor: "27AE60",
      title: "Normalization",
      items: [
        "All 18 tables in BCNF",
        "Lookup tables for domain values",
        "Junction tables for M:N relations",
        "V2 refinements applied"
      ]
    },
    {
      icon: icons.table, iconBg: C.accent, accentColor: C.accent,
      title: "Schema",
      items: [
        "20 tables with constraints",
        "30 foreign key relationships",
        "Referential integrity enforced",
        "3 SQL views for reporting"
      ]
    }
  ]);

  // 23. REFERENCES
  contentSlide("References", [
    "Silberschatz, Korth & Sudarshan \u2014 Database System Concepts (7th ed.)",
    "Elmasri & Navathe \u2014 Fundamentals of Database Systems (7th ed.)",
    "Connolly & Begg \u2014 Database Systems: A Practical Approach (6th ed.)",
    "C.J. Date \u2014 An Introduction to Database Systems (8th ed.)",
    "Ramakrishnan & Gehrke \u2014 Database Management Systems (3rd ed.)"
  ]);

  // 24. THANK YOU
  thankYouSlide();

  // SAVE
  const outPath = "/Users/dakshagarwal/dbms-project/laguna/report/Alumni_Network_Presentation.pptx";
  await prs.writeFile({ fileName: outPath });
  console.log("Presentation generated:", outPath);
  console.log("Total slides:", prs.slides.length);
}

build().catch(err => { console.error(err); process.exit(1); });
