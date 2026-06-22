"""Generate high-quality Meta & Google Ads dashboard mockup images for portfolio."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "meta google ads"
W, H = 1600, 900


def font(size, bold=False):
    names = ["arialbd.ttf", "Arial Bold.ttf", "arial.ttf", "Arial.ttf", "segoeui.ttf", "calibri.ttf"]
    if bold:
        names = ["arialbd.ttf", "Arial Bold.ttf"] + names
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded_rect(draw, xy, fill, radius=12, outline=None):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)


def bar_chart(draw, x, y, w, h, values, color):
    n = len(values)
    gap = 12
    bw = (w - gap * (n + 1)) // n
    mx = max(values) or 1
    for i, v in enumerate(values):
        bh = int((v / mx) * (h - 30))
        bx = x + gap + i * (bw + gap)
        by = y + h - bh
        draw.rounded_rectangle((bx, by, bx + bw, y + h - 8), radius=6, fill=color)
        draw.text((bx + bw // 2 - 8, y + h + 2), str(v), fill="#666", font=font(14))


def metric_card(draw, x, y, w, h, label, value, sub, accent):
    rounded_rect(draw, (x, y, x + w, y + h), "#ffffff", 14, "#e8edf3")
    draw.rectangle((x, y, x + 6, y + h), fill=accent)
    draw.text((x + 24, y + 22), label, fill="#667085", font=font(22))
    draw.text((x + 24, y + 58), value, fill="#101828", font=font(42, True))
    draw.text((x + 24, y + h - 34), sub, fill="#12b76a", font=font(18))


def header(draw, title, subtitle, bg, accent):
    draw.rectangle((0, 0, W, 88), fill=bg)
    draw.ellipse((W - 180, -40, W + 40, 180), fill=accent)
    draw.text((36, 24), title, fill="#ffffff", font=font(34, True))
    draw.text((36, 62), subtitle, fill="#dbeafe", font=font(20))


def save(img, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path, optimize=True)
    print(f"Created {path.name} ({img.size[0]}x{img.size[1]})")


def meta_campaign_overview():
    img = Image.new("RGB", (W, H), "#f4f6fb")
    d = ImageDraw.Draw(img)
    header(d, "Meta Ads Manager", "Campaign performance overview — Q2 2026", "#1877f2", "#0c5bd4")
    metric_card(d, 36, 120, 360, 130, "Amount Spent", "$4,280", "+18% vs last month", "#1877f2")
    metric_card(d, 416, 120, 360, 130, "ROAS", "3.8x", "+0.6x improvement", "#1877f2")
    metric_card(d, 796, 120, 360, 130, "Conversions", "312", "+24% growth", "#1877f2")
    metric_card(d, 1176, 120, 360, 130, "CTR", "2.14%", "Above benchmark", "#1877f2")
    rounded_rect(d, (36, 280, 1164, 820), "#ffffff", 16, "#e8edf3")
    d.text((56, 304), "Daily results", fill="#101828", font=font(28, True))
    bar_chart(d, 56, 360, 1060, 420, [42, 58, 51, 73, 68, 81, 77, 92, 88, 96], "#1877f2")
    rounded_rect(d, (1200, 280, 1564, 820), "#ffffff", 16, "#e8edf3")
    d.text((1220, 304), "Top ad sets", fill="#101828", font=font(24, True))
    rows = [("Lead Gen — Lahore", "ROAS 4.2x"), ("Retargeting — Cart", "ROAS 5.1x"), ("Lookalike 1%", "ROAS 3.4x")]
    for i, (a, b) in enumerate(rows):
        y = 360 + i * 120
        rounded_rect(d, (1220, y, 1544, y + 90), "#f8fafc", 12, "#e8edf3")
        d.text((1236, y + 18), a, fill="#101828", font=font(20, True))
        d.text((1236, y + 50), b, fill="#12b76a", font=font(18))
    save(img, "meta-campaign-overview.png")


def meta_audience_targeting():
    img = Image.new("RGB", (W, H), "#f4f6fb")
    d = ImageDraw.Draw(img)
    header(d, "Meta Ads Manager", "Audience targeting & ad set structure", "#1877f2", "#0c5bd4")
    rounded_rect(d, (36, 120, 780, 820), "#ffffff", 16, "#e8edf3")
    d.text((56, 144), "Audience breakdown", fill="#101828", font=font(28, True))
    slices = [("Interest: Business owners", 38, "#1877f2"), ("Lookalike purchasers", 27, "#60a5fa"), ("Retargeting 30d", 22, "#93c5fd"), ("Broad advantage+", 13, "#bfdbfe")]
    y = 210
    for label, pct, color in slices:
        rounded_rect(d, (56, y, 760, y + 72), "#f8fafc", 12, "#e8edf3")
        d.rectangle((56, y, 56 + int(6.8 * pct), y + 72), fill=color)
        d.text((80, y + 22), f"{label}  —  {pct}%", fill="#101828", font=font(22))
        y += 92
    rounded_rect(d, (820, 120, 1564, 820), "#ffffff", 16, "#e8edf3")
    d.text((840, 144), "Placement performance", fill="#101828", font=font(28, True))
    bar_chart(d, 840, 220, 680, 520, [88, 72, 64, 91, 55], "#1877f2")
    labels = ["Feed", "Stories", "Reels", "Marketplace", "Audience Network"]
    for i, lb in enumerate(labels):
        d.text((860 + i * 130, 760), lb, fill="#667085", font=font(16))
    save(img, "meta-audience-targeting.png")


def meta_ad_creatives():
    img = Image.new("RGB", (W, H), "#f4f6fb")
    d = ImageDraw.Draw(img)
    header(d, "Meta Ads Manager", "Creative testing & A/B performance", "#1877f2", "#0c5bd4")
    creatives = [
        ("Creative A — Video hook", "CTR 2.8%", "CPC $0.42", "#1877f2"),
        ("Creative B — Carousel", "CTR 2.1%", "CPC $0.51", "#60a5fa"),
        ("Creative C — Static offer", "CTR 1.7%", "CPC $0.63", "#93c5fd"),
    ]
    x = 36
    for title, ctr, cpc, color in creatives:
        rounded_rect(d, (x, 130, x + 480, 820), "#ffffff", 16, "#e8edf3")
        rounded_rect(d, (x + 24, 160, x + 456, 520), color, 12)
        d.text((x + 40, 560), title, fill="#101828", font=font(24, True))
        d.text((x + 40, 610), ctr, fill="#12b76a", font=font(28, True))
        d.text((x + 40, 660), cpc, fill="#667085", font=font(22))
        d.text((x + 40, 720), "Winner: scaling budget +35%", fill="#101828", font=font(18))
        x += 520
    save(img, "meta-ad-creatives.png")


def google_ads_overview():
    img = Image.new("RGB", (W, H), "#f8fafc")
    d = ImageDraw.Draw(img)
    header(d, "Google Ads", "Search & Performance Max campaign overview", "#1a73e8", "#1558b0")
    metric_card(d, 36, 120, 360, 130, "Cost", "$3,960", "-9% waste reduced", "#1a73e8")
    metric_card(d, 416, 120, 360, 130, "Conv. rate", "4.6%", "+1.1 pts", "#1a73e8")
    metric_card(d, 796, 120, 360, 130, "CPA", "$12.70", "Below target", "#1a73e8")
    metric_card(d, 1176, 120, 360, 130, "Impr. share", "78%", "Top of page 61%", "#1a73e8")
    rounded_rect(d, (36, 280, 1564, 820), "#ffffff", 16, "#e8edf3")
    d.text((56, 304), "Conversion trend (last 14 days)", fill="#101828", font=font(28, True))
    bar_chart(d, 80, 360, 1400, 420, [18, 24, 22, 31, 28, 35, 33, 41, 39, 44, 48, 52, 50, 57], "#1a73e8")
    save(img, "google-ads-overview.png")


def google_ads_keywords():
    img = Image.new("RGB", (W, H), "#f8fafc")
    d = ImageDraw.Draw(img)
    header(d, "Google Ads", "Keyword planner & search terms report", "#1a73e8", "#1558b0")
    rounded_rect(d, (36, 120, 980, 820), "#ffffff", 16, "#e8edf3")
    d.text((56, 144), "Top performing keywords", fill="#101828", font=font(28, True))
    headers = ["Keyword", "Clicks", "Conv.", "CPA"]
    cols = [56, 420, 620, 780]
    y = 210
    for i, h in enumerate(headers):
        d.text((cols[i], y), h, fill="#667085", font=font(20, True))
    rows = [
        ("email marketing freelancer", "842", "46", "$11.20"),
        ("linkedin lead generation", "613", "31", "$13.40"),
        ("meta ads specialist", "528", "27", "$12.05"),
        ("upwork profile optimization", "401", "19", "$14.80"),
        ("google ads management", "377", "22", "$10.95"),
    ]
    y = 260
    for row in rows:
        rounded_rect(d, (56, y, 960, y + 72), "#f8fafc", 10, "#edf2f7")
        for i, cell in enumerate(row):
            d.text((cols[i], y + 22), cell, fill="#101828", font=font(20))
        y += 88
    rounded_rect(d, (1020, 120, 1564, 820), "#ffffff", 16, "#e8edf3")
    d.text((1040, 144), "Quality Score distribution", fill="#101828", font=font(24, True))
    bar_chart(d, 1040, 220, 480, 520, [12, 28, 44, 36, 18], "#34a853")
    save(img, "google-ads-keywords.png")


def ads_performance_roas():
    img = Image.new("RGB", (W, H), "#f4f6fb")
    d = ImageDraw.Draw(img)
    header(d, "Cross-Channel Ads Report", "Meta + Google blended performance", "#7c3aed", "#5b21b6")
    metric_card(d, 36, 120, 360, 130, "Total spend", "$8,240", "Across 6 campaigns", "#7c3aed")
    metric_card(d, 416, 120, 360, 130, "Revenue", "$31,420", "Tracked conversions", "#7c3aed")
    metric_card(d, 796, 120, 360, 130, "Blended ROAS", "3.81x", "Above 3.0x goal", "#7c3aed")
    metric_card(d, 1176, 120, 360, 130, "Leads", "428", "+31% MoM", "#7c3aed")
    rounded_rect(d, (36, 280, 760, 820), "#ffffff", 16, "#e8edf3")
    d.text((56, 304), "Channel split", fill="#101828", font=font(28, True))
    bar_chart(d, 80, 380, 620, 380, [58, 42], "#1877f2")
    d.text((220, 780), "Meta Ads", fill="#667085", font=font(20))
    d.text((420, 780), "Google Ads", fill="#667085", font=font(20))
    rounded_rect(d, (800, 280, 1564, 820), "#ffffff", 16, "#e8edf3")
    d.text((820, 304), "Optimization actions applied", fill="#101828", font=font(28, True))
    actions = [
        "Paused 4 underperforming ad sets",
        "Increased budget on top 2 creatives",
        "Added negative keywords (-18% waste)",
        "Launched retargeting funnel for cart abandoners",
    ]
    y = 380
    for action in actions:
        rounded_rect(d, (820, y, 1544, y + 78), "#f5f3ff", 12, "#ddd6fe")
        d.text((840, y + 26), "•  " + action, fill="#101828", font=font(20))
        y += 98
    save(img, "ads-performance-roas.png")


if __name__ == "__main__":
    meta_campaign_overview()
    meta_audience_targeting()
    meta_ad_creatives()
    google_ads_overview()
    google_ads_keywords()
    ads_performance_roas()
    print("All Meta & Google Ads portfolio images generated.")
