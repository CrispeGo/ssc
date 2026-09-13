#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract ALL Mathematics questions from every available paper into master JSON.
Reuses the layout-aware extractors built for Physics (same paper families)."""
import os, json
import extract_physics as ep

AG = '/home/user/agniveer'

R25 = range(1, 26)
R12 = range(1, 13)

papers = [
    # SelfStudys 70Q papers: Math = Q26-50 ; 34Q papers: Math = Q13-24
    ('X', '2020-11-04', '04 Nov 2020', 'SelfStudys', 'Group_X_2020_04-Nov.pdf', 'selfstudys', range(26, 51)),
    ('X', '2021-07-18', '18 Jul 2021', 'SelfStudys', 'Group_X_2021_18-Jul.pdf', 'selfstudys', range(26, 51)),
    ('X', '2022-07-25', '25 Jul 2022', 'SelfStudys', 'Group_X_2022_25-Jul.pdf', 'selfstudys', range(26, 51)),
    ('X', '2023-01-18', '18 Jan 2023', 'SelfStudys', 'Group_X_2023_18-Jan.pdf', 'selfstudys', range(26, 51)),
    ('X', '2023-01-19', '19 Jan 2023', 'SelfStudys', 'Group_X_2023_19-Jan.pdf', 'selfstudys', range(26, 51)),
    ('X', '2023-10-13', '13 Oct 2023 Shift-1', 'SelfStudys', 'Group_X_2023_13-Oct_Shift-1.pdf', 'selfstudys', range(13, 25)),
    ('X', '2023-10-14', '14 Oct 2023 Shift-1', 'SelfStudys', 'Group_X_2023_14-Oct_Shift-1.pdf', 'selfstudys', range(13, 25)),
    ('X', '2024-11-16', '16 Nov 2024', 'SelfStudys', 'Group_X_2024_16-Nov.pdf', 'selfstudys', range(26, 51)),
    ('X', '2025-03-22', '22 Mar 2025', 'SelfStudys', 'Group_X_2025_22-Mar.pdf', 'selfstudys', range(26, 51)),
    # Prepp 2020 official papers: Math = Que.46-70
    ('X', '2020-11-04', '04 Nov 2020', 'Prepp', 'prepp/Group_X_2020_04-Nov.pdf', 'prepp', range(46, 71)),
    ('X', '2020-11-05', '05 Nov 2020', 'Prepp', 'prepp/Group_X_2020_05-Nov.pdf', 'prepp', range(46, 71)),
    ('X', '2020-11-06', '06 Nov 2020', 'Prepp', 'prepp/Group_X_2020_06-Nov.pdf', 'prepp', range(46, 71)),
    ('X', '2020-11-07', '07 Nov 2020', 'Prepp', 'prepp/Group_X_2020_07-Nov.pdf', 'prepp', range(46, 71)),
    # Prepp 2021 memory papers: Math = Que.26-50 (13-Jul S1 = Que.46-70)
    ('X', '2021-07-12', '12 Jul 2021 Shift-2', 'Prepp', 'prepp/Group_X_2021_12-Jul_S2.pdf', 'prepp', range(26, 51)),
    ('X', '2021-07-13', '13 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_13-Jul_S1.pdf', 'prepp', range(46, 71)),
    ('X', '2021-07-13', '13 Jul 2021 Shift-2', 'Prepp', 'prepp/Group_X_2021_13-Jul_S2.pdf', 'prepp', range(26, 51)),
    ('X', '2021-07-14', '14 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_14-Jul_S1.pdf', 'prepp', range(26, 51)),
    ('X', '2021-07-14', '14 Jul 2021 Shift-3', 'Prepp', 'prepp/Group_X_2021_14-Jul_S3.pdf', 'prepp', range(26, 51)),
    ('X', '2021-07-15', '15 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_15-Jul_S1.pdf', 'prepp', range(26, 51)),
    ('X', '2021-07-15', '15 Jul 2021 Shift-3', 'Prepp', 'prepp/Group_X_2021_15-Jul_S3.pdf', 'prepp', range(26, 51)),
    ('X', '2021-07-18', '18 Jul 2021 Shift-1', 'Prepp', 'prepp/Group_X_2021_18-Jul_S1.pdf', 'prepp', range(26, 51)),
    ('X', '2021-07-18', '18 Jul 2021 Shift-3', 'Prepp', 'prepp/Group_X_2021_18-Jul_S3.pdf', 'prepp', range(26, 51)),
    # Utkarsh X papers: Math = Q26-50
    ('X', '2024-03-17', '17 Mar 2024 Shift-1', 'Utkarsh', 'utkarsh/Group_X_2024_17-Mar_Shift-1.pdf', 'utkarsh_x', range(26, 51)),
    ('X', '2025-09-25', '25 Sep 2025', 'Utkarsh', 'utkarsh/Group_X_2025_25-Sep_Shift-A.pdf', 'utkarsh_x', range(26, 51)),
    ('X', '2025-09-27', '27 Sep 2025', 'Utkarsh', 'utkarsh/Group_X_2025_27-Sep.pdf', 'utkarsh_x', range(26, 51)),
    # Utkarsh XY: Math section (25 questions)
    ('XY', '2026-03-30', '30 Mar 2026', 'Utkarsh', 'utkarsh/Group_XY_2026_30-Mar_OtherThanScience.pdf', 'utkarsh_xy_math', range(1, 26)),
    # User TXT (verbatim): Math = Q26-50
    ('XY', '2024-11-16', '16 Nov 2024', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_16_Nov_2024_Fresh_Verified.txt', 'user_txt', range(26, 51)),
    ('XY', '2025-03-22', '22 Mar 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_22_Mar_2025_All_Questions.txt', 'user_txt', range(26, 51)),
    ('XY', '2025-09-25', '25 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_25_Sep_2025_Fresh_Verified.txt', 'user_txt', range(26, 51)),
    ('XY', '2025-09-26', '26 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_26_Sep_2025_Fresh_Verified.txt', 'user_txt', range(26, 51)),
    ('XY', '2025-09-27', '27 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_27_Sep_2025_Fresh_Verified.txt', 'user_txt', range(26, 51)),
    ('XY', '2025-09-28', '28 Sep 2025', 'User TXT', 'user_txt/Agniveer_Vayu_Group_XY_28_Sep_2025_Fresh_Verified.txt', 'user_txt', range(26, 51)),
    # Prepp official Mathematics sample paper
    ('X', 'MODEL', 'Sample Mathematics Paper', 'Prepp Sample', 'prepp/Sample_X_Maths.pdf', 'sample', range(1, 26)),
]

extractors = {
    'selfstudys': ep.extract_selfstudys,
    'prepp': ep.extract_prepp,
    'utkarsh_x': ep.extract_utkarsh_x,
    'utkarsh_xy_math': lambda p, r: ep.extract_utkarsh_xy(p, 'Section : Mathematics', 'Section : English', r),
    'user_txt': ep.extract_user_txt,
    'sample': ep.extract_sample_physics,
}

def _q(q, opts, ans=''):
    return {'q': q, 'opts': opts, 'ans': ans}

# Math symbol glyphs (private-use area) -> readable Unicode, as used across the
# Utkarsh / Sample PDFs. Same code can mean different glyphs in different files,
# so ambiguous ones are only handled via MANUAL entries, never here.
MATH_SYM = {
    '\uf0f2': '∫',           # integral
    '\uf0e6': '(', '\uf0f6': ')', '\uf0e7': '(', '\uf0f7': ')', '\uf0e8': '(', '\uf0f8': ')',  # big paren pieces
    '\uf0e9': '[', '\uf0f9': ']', '\uf0ea': '[', '\uf0fa': ']', '\uf0eb': '[', '\uf0fb': ']',  # matrix brackets
    '\uf0ec': '{', '\uf0fc': '}', '\uf0ed': '{', '\uf0fd': '}', '\uf0ee': '{', '\uf0fe': '}',  # brace pieces
    '\uf070': 'π', '\uf0c8': '∪', '\uf0ce': '∈', '\uf0b9': '≠', '\uf0ae': '→',
    '\uf02d': '−', '\uf02b': '+', '\uf03d': '=', '\uf028': '(', '\uf029': ')',
    '\uf07b': '{', '\uf07d': '}', '\uf077': 'ω', '\uf0d9': 'î', '\uf0b4': '×',
}

def _clean_sym(s):
    for k, v in MATH_SYM.items():
        s = s.replace(k, v)
    return s

MANUAL = {
    ('22 Mar 2025', 'SelfStudys', 1): _q(
        "Let A = [[1, 0, 0], [5, 2, 0], [−1, 6, 1]], then the adjoint of A is:",
        ["[[2, −5, 32], [0, 1, −6], [0, 0, 2]]",
         "[[−1, 0, 0], [0, −2, 0], [0, −6, 1]]",
         "[[−1, 1, 0], [−5, −2, 0], [1, −6, −1]]",
         "None of these"], "D"),
    ('04 Nov 2020', 'SelfStudys', 15): _q(
        "Find the value of x and y if [x + 3y, y] = [4, −1] ?",
        ["x = 2 and y = 5", "x = −7 and y = 1", "x = 7 and y = −1", "x = −5 and y = −2"], "C"),
    ('13 Oct 2023 Shift-1', 'SelfStudys', 10): _q(
        "Find the value of →a × →a",
        ["1", "0", "|→a|", "|→a|²"], "B"),
    ('06 Nov 2020', 'Prepp', 5): _q(
        "If a line has the direction ratios (2, -3, 4) then its direction cosines are",
        ["(2/√25, −3/√25, 4/√25)", "(2/√29, 3/√29, 4/√29)", "(2/√29, −3/√29, 4/√29)", "None of the above"], "C"),
    # ---------------- Utkarsh 17 Mar 2024 ----------------
    ('17 Mar 2024 Shift-1', 'Utkarsh', 4): _q(
        "The value of ∫₀² x³/(x + 1) dx is",
        ["8/3 + ln 3", "8/3 + ln 3", "8/3 − ln 3", "8/3 − ln 3"], "C"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 5): _q(
        "The coefficient of the term independent of x in the expansion of (x + 1/x)¹⁰ is equal to",
        ["10", "252", "20", "256"], "B"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 7): _q(
        "What is the order and degree of the equation (d³y/dx³)² = (d²y/dx²)³, respectively?",
        ["2, 3", "1, 3", "3, 1", "3, 2"], "D"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 11): _q(
        "If A = [[i, 0], [0, −i]], then the value of A⁻¹ is",
        ["[[i, 0], [i, 0]]", "[[−i, 0], [0, i]]", "[[i, 0], [0, −i]]", "[[i, 0], [0, i]]"], "B"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 15): _q(
        "∫ x³/(a² + x²) dx = ?",
        ["√(a² + x²) + C", "1/(a² − x²) + c", "√(a² − x²) + C", "1/(a² + x²) + c"], ""),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 16): _q(
        "If a⃗ = xî + yĵ + zk̂, then (a⃗·î)î + (a⃗·ĵ)ĵ + (a⃗·k̂)k̂ = ?",
        ["−a⃗", "a⃗", "1", "None of these"], "B"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 24): _q(
        "If the direction ratios of two lines are (1, 2, 3) and (-2, 3, -4), then the angle between the lines is:",
        ["cos⁻¹(8/√406)", "cos⁻¹(−8/√406)", "cos⁻¹(−6/√406)", "cos⁻¹(6/√406)"], "A"),
    ('17 Mar 2024 Shift-1', 'Utkarsh', 25): _q(
        "What is lim x→4  (3 − √(5 + x)) / (x − 4)  equal to?",
        ["−1/2", "−1/6", "1/6", "−1/5"], "B"),
    # ---------------- Utkarsh 25 Sep 2025 ----------------
    ('25 Sep 2025', 'Utkarsh', 14): _q(
        "The volume of a spherical ball is increasing at the rate of 4π cc/sec. Then the rate of increase of its surface area, when the volume is 288π cc, is:",
        ["3π/4 cm²/sec", "4/3 cm²/sec", "4π/3 cm²/sec", "3/4 cm²/sec"], "C"),
    ('25 Sep 2025', 'Utkarsh', 15): _q(
        "If A = {1, 3, 6} and B = {5, 6}, then (A ∪ B) will be:",
        ["{1, 2, 3, 4, 5}", "{2, 4}", "{1, 3, 5, 6}", "{2, 4, 5}"], "C"),
    ('25 Sep 2025', 'Utkarsh', 24): _q(
        "The domain of sin⁻¹x is",
        ["(−π, π)", "[−1, 1]", "(0, 2π)", "(−∞, ∞)"], "B"),
    # ---------------- Utkarsh 27 Sep 2025 ----------------
    ('27 Sep 2025', 'Utkarsh', 7): _q(
        "If A = [[a, b], [c, d]], then adj(Aᵀ) − (adj A)ᵀ is",
        ["[[0, 0], [0, 0]]", "[[a, b], [c, d]]", "[[1, 0], [0, 1]]", "2(ad − bc)[[1, 0], [0, 1]]"], "A"),
    ('27 Sep 2025', 'Utkarsh', 12): _q(
        "The value of k which makes the function  f(x) = { x·sin(1/x), if x ≠ 0 ;  k, if x = 0 }  continuous at x = 0 is:",
        ["8", "1", "−1", "None of the above"], "D"),
    ('27 Sep 2025', 'Utkarsh', 18): _q(
        "The range of tan⁻¹x is",
        ["(π/2, π)", "(−π/2, π/2)", "(−π, π)", "(0, π)"], "B"),
    ('27 Sep 2025', 'Utkarsh', 20): _q(
        "If A = [[−1, 2], [3, 4]] and B = [[1, 2], [1, 0]], then A + B = ?",
        ["[[−2, 0], [2, 4]]", "[[0, 4], [4, 4]]", "[[−1, 4], [3, 0]]", "[[1, 0], [0, 1]]"], "B"),
    # ---------------- Utkarsh 30 Mar 2026 (XY) ----------------
    ('30 Mar 2026', 'Utkarsh', 12): _q(
        "Evaluate ∫₀¹ dx / (x + √(1 − x²))",
        ["π/3", "π/4", "π/2", "π/6"], "B"),
    ('30 Mar 2026', 'Utkarsh', 20): _q(
        "If f(x) = sin(cos²(πx)), find the value of f'(1/4).",
        ["−π cos(1/2)", "−π sin(1/2)·cos(1/2)", "−π sin(1/2)", "0"], "A"),
    ('30 Mar 2026', 'Utkarsh', 22): _q(
        "Evaluate ∫ [(x + 2)² + (x − 1)] dx",
        ["(x + 2)³/3 + (x − 1)²/2 + c", "(x + 2)³/3 − (x − 1)²/2 + c",
         "(x + 2)²/2 + (x − 1)²/2 + c", "(x + 2)³/3 + 2(x − 1)²/9 + c"], "A"),
    ('30 Mar 2026', 'Utkarsh', 23): _q(
        "Which term in the expansion of (x² + 1/x)¹² is independent of x?",
        ["6th", "9th", "7th", "8th"], "B"),
    # ---------------- Sample Mathematics Paper ----------------
    ('Sample Mathematics Paper', 'Prepp Sample', 1): _q(
        "What is the nature of relation R, if R is defined as R = {(x, y) : 2x + y = 41, x, y ∈ N}?",
        ["Reflexive", "Symmetric", "Transitive", "None of these"], "D"),
    ('Sample Mathematics Paper', 'Prepp Sample', 2): _q(
        "cos 24° + cos 55° + cos 125° + cos 204° + cos 300° = ?",
        ["1/2", "3/2", "3", "0"], "A"),
    ('Sample Mathematics Paper', 'Prepp Sample', 3): _q(
        "sec⁻¹[(x² + 1)/(x² − 1)] = ?",
        ["2 tan⁻¹x", "2x²", "2 cot⁻¹x", "x²"], "C"),
    ('Sample Mathematics Paper', 'Prepp Sample', 4): _q(
        "Find the foci of hyperbola 9x² − 16y² = 144.",
        ["(0, ±5)", "(±5, 0)", "(±5, 1)", "(5, ±1)"], "B"),
    ('Sample Mathematics Paper', 'Prepp Sample', 5): _q(
        "Find the nature of the triangle whose vertices are A(12, 8), B(−2, 6) and C(6, 0).",
        ["Isosceles right-angle triangle", "Equilateral triangle", "Scalene triangle", "None of these"], "A"),
    ('Sample Mathematics Paper', 'Prepp Sample', 6): _q(
        "For every point P(x, y, z) on the xy-plane,",
        ["x = 0", "y = 0", "z = 0", "None of these"], "C"),
    ('Sample Mathematics Paper', 'Prepp Sample', 7): _q(
        "Find the conjugate of (6 + 5i)².",
        ["60 + 11i", "11 − 60i", "11 + 60i", "60 − 11i"], "B"),
    ('Sample Mathematics Paper', 'Prepp Sample', 8): _q(
        "C(n, r) + 2·C(n, r−1) + C(n, r−2) = ?",
        ["C(n+1, r)", "C(n+2, r)", "C(n+2, r−1)", "C(n+1, r−1)"], "B"),
    ('Sample Mathematics Paper', 'Prepp Sample', 9): _q(
        "If the nth term of a G.P. is 2ⁿ, then find the sum of its first 6 terms.",
        ["126", "124", "190", "154"], "A"),
    ('Sample Mathematics Paper', 'Prepp Sample', 10): _q(
        "Find the coefficient of x² in the expansion of (3x − 1/x)⁶.",
        ["405", "7290", "2430", "1215"], "D"),
    ('Sample Mathematics Paper', 'Prepp Sample', 11): _q(
        "Evaluate the determinant  |0 a b; a 0 c; b c 0| .",
        ["a²b²c²", "4a²b²c²", "(1/4)a²b²c²", "(a + b + c)²"], "B"),
    ('Sample Mathematics Paper', 'Prepp Sample', 12): _q(
        "If A = [[0, 0, 1], [0, 1, 0], [1, 0, 0]], then A⁻¹ = ?",
        ["A", "−A", "I", "−I"], "A"),
    ('Sample Mathematics Paper', 'Prepp Sample', 13): _q(
        "If ω is the cube root of unity, then  |1 1 1; 1 ω ω²; 1 ω² ω| = ?",
        ["1", "ω", "ω²", "0"], "D"),
    ('Sample Mathematics Paper', 'Prepp Sample', 14): _q(
        "lim x→0  [sin(2 + x) − sin(2 − x)] / x  = ?",
        ["(1/2)cos 2", "1", "2 cos 2", "0"], "C"),
    ('Sample Mathematics Paper', 'Prepp Sample', 15): _q(
        "d/dx [tan⁻¹(sec x + tan x)] = ?",
        ["−1/2", "1", "−1", "1/2"], "D"),
    ('Sample Mathematics Paper', 'Prepp Sample', 16): _q(
        "Find d²y/dx², if x + y = c − xy.",
        ["2c", "−2/c²", "2/c²", "4/c²"], "C"),
    ('Sample Mathematics Paper', 'Prepp Sample', 17): _q(
        "An edge of a cube is increasing at the rate of 3 cm/sec. Find the rate at which the volume increases (in cm³/sec) if the edge of the cube is 10 cm.",
        ["900", "725", "700", "825"], "A"),
    ('Sample Mathematics Paper', 'Prepp Sample', 18): _q(
        "If s = t³ − 4t² + 5 describes the motion of a particle, then its velocity (in unit/sec) when the acceleration vanishes, is:",
        ["16/9", "−32/3", "4/3", "−16/3"], "D"),
    ('Sample Mathematics Paper', 'Prepp Sample', 19): _q(
        "Find the standard deviation of 8, 12, 13, 15, 22.",
        ["3.54", "3.72", "4.21", "4.6"], "D"),
    ('Sample Mathematics Paper', 'Prepp Sample', 20): _q(
        "If a coin is tossed thrice, find the probability of getting one or two heads.",
        ["4/5", "5/8", "3/4", "6/7"], "C"),
    ('Sample Mathematics Paper', 'Prepp Sample', 21): _q(
        "If the points A = 60î + 3ĵ, B = 40î − 8ĵ, and C = aî − 52ĵ are collinear, then a is equal to:",
        ["40", "−40", "20", "−20"], "B"),
    ('Sample Mathematics Paper', 'Prepp Sample', 22): _q(
        "∫ sin²x dx = ?  (limits: −π/3 to π/3)",
        ["1", "(3√3 − π)/4", "(2 − π)/4", "0"], "B"),
    ('Sample Mathematics Paper', 'Prepp Sample', 23): _q(
        "∫ cos 2x / (sin²x · cos²x) dx = ?",
        ["−cot x − tan x + c", "−cot x + tan x + c", "cot x + tan x + c", "tan x − cot x + c"], "A"),
    ('Sample Mathematics Paper', 'Prepp Sample', 24): _q(
        "Find the solution of the differential equation  dy/dx = e^(x+y) + x²e^y .",
        ["e^(−y) = e^x − x³/3 + c", "e^(−y) = e^x + x³/3 + c",
         "e^(−y) = −e^x − x³/3 + c", "e^(−y) = −e^x + x³/3 + c"], "C"),
    ('Sample Mathematics Paper', 'Prepp Sample', 25): _q(
        "Find the area of the region (in sq. units) bounded by the curve y = 2x − x² and the y-axis.",
        ["8/3", "4/3", "5/3", "2/3"], "B"),
    # ---------------- matrix questions reconstructed from PDF span data ----------------
    ('18 Jul 2021', 'SelfStudys', 16): _q(
        "Construct a 3 × 2 matrix whose elements are given by aᵢⱼ = (1/3)|2i + j|",
        ["[[1, 5/3], [4/3, 2], [7/3, 8/3]]", "[[1, 4/3], [7/3, 2], [5/3, 8/3]]",
         "[[1, 4/3], [5/3, 2], [8/3, 7/3]]", "[[1, 4/3], [5/3, 2], [7/3, 8/3]]"], "D"),
    ('18 Jul 2021 Shift-3', 'Prepp', 16): _q(
        "Construct a 3 × 2 matrix whose elements are given by aᵢⱼ = (1/3)|2i + j|",
        ["[[1, 5/3], [4/3, 2], [7/3, 8/3]]", "[[1, 4/3], [7/3, 2], [5/3, 8/3]]",
         "[[1, 4/3], [5/3, 2], [8/3, 7/3]]", "[[1, 4/3], [5/3, 2], [7/3, 8/3]]"], "D"),
    ('25 Jul 2022', 'SelfStudys', 18): _q(
        "If A = [[1, 3, 3], [1, 4, 3], [1, 3, 4]], then adj(A) is",
        ["[[7, −3, −3], [−1, 1, 0], [−1, 0, 1]]", "[[7, 3, 3], [−1, 1, 0], [−1, 0, −1]]",
         "[[7, −3, −3], [1, 1, 0], [−1, 0, 1]]", "[[−7, 3, −3], [−1, 1, 0], [−1, 0, −1]]"], "A"),
    ('14 Oct 2023 Shift-1', 'SelfStudys', 11): _q(
        "If a, b, c are non-zero real numbers, then the inverse of the matrix A = [[a, 0, 0], [0, b, 0], [0, 0, c]] is equal to",
        ["[[1/a, 0, 0], [0, 1/b, 0], [0, 0, 1/c]]", "(1/abc)·[[1/a, 0, 0], [0, 1/b, 0], [0, 0, 1/c]]",
         "(1/abc)·[[1, 0, 0], [0, 1, 0], [0, 0, 1]]", "(1/abc)·[[a, 0, 0], [0, b, 0], [0, 0, c]]"], "A"),
    ('18 Jan 2023', 'SelfStudys', 20): _q(
        "For matrix A = [[2, 5], [−11, 7]], (adj A)′ is equal to:",
        ["[[−2, −5], [11, −7]]", "[[7, 5], [11, 2]]", "[[7, 11], [−5, 2]]", "[[7, −5], [11, 2]]"], "C"),
    ('18 Jan 2023', 'SelfStudys', 21): _q(
        "The inverse of matrix A, where A = [[2, 5], [1, 3]], is",
        ["[[3, 5], [−1, 2]]", "[[3, −5], [−1, 2]]", "[[3, −5], [1, 2]]", "[[−2, 1], [5, 3]]"], "B"),
    ('19 Jan 2023', 'SelfStudys', 20): _q(
        "The inverse of a matrix A is given by [[−2, 1], [3/2, −1/2]]. What is A equal to?",
        ["[[1, 2], [3, 4]]", "[[1, −2], [−3, 4]]", "[[1, 2], [3, −4]]", "[[−1, 2], [3, 4]]"], "A"),
    ('16 Nov 2024', 'SelfStudys', 14): _q(
        "The inverse of the matrix [[2 + 3i, −i], [i, 2 − 3i]] is:",
        ["(1/12)[[2 − 3i, i], [−i, −2 + 3i]]", "(1/12)[[2 − 3i, i], [−i, 2 + 3i]]",
         "(1/12)[[2 + 3i, i], [−i, 2 − 3i]]", "(1/12)[[2 − 3i, −i], [i, 2 + 3i]]"], "B"),
    ('14 Jul 2021 Shift-1', 'Prepp', 10): _q(
        "If x + 2y = [[2, −3], [1, 5]] and 2x + 5y = [[7, 5], [2, 3]], then y is equal to ?",
        ["[[3, 11], [0, 7]]", "[[3, 5], [0, −7]]", "[[3, 11], [0, −7]]", "[[3, 5], [0, 7]]"], "C"),
    ('15 Jul 2021 Shift-3', 'Prepp', 12): _q(
        "If A = [[0, −1], [−1, 0]], then A² is equal to",
        ["[[0, 1], [1, 0]]", "[[1, 0], [0, 1]]", "[[−1, 0], [0, −1]]", "[[0, −1], [−1, 0]]"], "B"),
    ('18 Jul 2021 Shift-1', 'Prepp', 18): _q(
        "If A = [[1, −2], [−1, 2]] and B = [[2, 6], [1, 3]], then AB is equal to",
        ["[[0, 0], [0, 0]]", "[[1, 0], [0, 1]]", "[[1, 1], [1, 1]]", "None of the above"], "A"),
    ('13 Oct 2023 Shift-1', 'SelfStudys', 3): _q(
        "If the sum of the matrices [x, x, y], [y, y, z] and [z, 0, 0] is the matrix [10, 5, 5], then what is the value of y?",
        ["−5", "0", "5", "10"], "B"),
    ('16 Nov 2024', 'SelfStudys', 2): _q(
        "Find the value of det(3A) for the following matrix A = [[4, 7, 1], [−1, 3, 2], [−2, 0, 5]]",
        ["1458", "81", "27", "1971"], "D"),
    ('22 Mar 2025', 'SelfStudys', 23): _q(
        "If A = [[1, −1, 1], [2, −1, 0], [1, 0, 0]], then A⁵ =",
        ["A", "Identity Matrix", "Null Matrix", "A⁻¹"], "D"),
    # ---------------- fraction-layout questions reconstructed from span data ----------------
    ('04 Nov 2020', 'SelfStudys', 6): _q(
        "∫ √(ax + b) dx is equal to ?",
        ["(ax + b)^(3/2)/(3a) + c", "2(ax + b)^(3/2)/3 + c", "2(ax + b)^(3/2)/(3a) + c", "None of the above"], "C"),
    ('18 Jan 2023', 'SelfStudys', 15): _q(
        "Value of ∫ x log x dx is",
        ["(x²/2)·log x − x²/4 + C", "(x/2)·log x − x/4 + C", "x²·log x − 4x + C", "(log x)²/2 − x²/4 + C"], "A"),
    ('14 Oct 2023 Shift-1', 'SelfStudys', 6): _q(
        "∫ x³e^(x²) dx =",
        ["(1/2)(x² + 1)e^(x²) + c", "(x² + 1)e^(x²) + c", "(1/2)(x² − 1)e^(x²) + c", "(x² − 1)e^(x²) + c"], "C"),
    ('13 Jul 2021 Shift-2', 'Prepp', 19): _q(
        "For x ∈ (−3π/2, π/2), the expression cot⁻¹((1 − sin x)/cos x) can be simplified as:",
        ["π/4 + x/2", "π/4 − x/2", "tan x", "tan(−x)"], "A"),
    ('14 Jul 2021 Shift-1', 'Prepp', 22): _q(
        "The area of the parallelogram whose diagonals are a⃗ = 3î + ĵ − 2k̂ and b⃗ = î − 3ĵ + 4k̂ is:",
        ["10√3", "5√3", "√(10/2)", "√(5/2)"], "B"),
    ('14 Jul 2021 Shift-3', 'Prepp', 4): _q(
        "Evaluate: ∫ dx / √(x² − 49)",
        ["ln|x + √(x² − 49)| + C", "ln|x − √(x² − 49)| + C", "(1/7)ln|x + √(x² − 49)| + C", "(1/7)ln|x − √(x² − 49)| + C"], "A"),
}

ANS_OVERRIDES = {
    ('17 Mar 2024 Shift-1', 'Utkarsh', 2): 'A',  # y=(sinx)^y -> dy/dx = y²cotx/(1−y·ln sinx)
}

# Questions whose answer marker was lost in the source OCR and could not be
# recovered with certainty (left blank rather than guessed).
KNOWN_BLANK = {
    ('17 Mar 2024 Shift-1', 'Utkarsh', 15),  # integral, integrand garbled in source
}

def main():
    results = []
    for grp, key, label, src, rel, kind, qrange in papers:
        path = os.path.join(AG, rel)
        if not os.path.exists(path):
            results.append({'grp': grp, 'key': key, 'label': label, 'src': src, 'qs': None, 'err': 'FILE MISSING'})
            continue
        try:
            qs = extractors[kind](path, qrange)
            for i, q in enumerate(qs, 1):
                ov = MANUAL.get((label, src, i))
                if ov and q is not None:
                    qs[i - 1] = ov
                ao = ANS_OVERRIDES.get((label, src, i))
                if ao and q is not None:
                    q['ans'] = ao
            # clean leftover symbol glyphs (PUA) on non-manual entries
            for q in qs:
                if q is None or 'raw' in q:
                    continue
                q['q'] = _clean_sym(q.get('q') or '')
                q['opts'] = [_clean_sym(o) for o in (q.get('opts') or [])]
            results.append({'grp': grp, 'key': key, 'label': label, 'src': src, 'qs': qs, 'err': ''})
        except Exception as ex:
            results.append({'grp': grp, 'key': key, 'label': label, 'src': src, 'qs': None, 'err': str(ex)})
    json.dump(results, open('/home/user/_math_raw.json', 'w'), ensure_ascii=False, indent=1)
    print("PAPER                              GROUP  SOURCE       EXTRACTED")
    for r in results:
        qs = r['qs']
        cnt = sum(1 for x in (qs or []) if x is not None) if qs else 0
        total = len(qs) if qs else 0
        flag = ('  <-- ' + r['err']) if r['err'] else ''
        print(f"{r['label']:32s}  {r['grp']:5s}  {r['src']:12s}  {cnt}/{total}{flag}")
    return results

if __name__ == '__main__':
    main()
