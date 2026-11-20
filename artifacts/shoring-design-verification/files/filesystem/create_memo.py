from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

src = '/filesystem/Thelbridge_Verification_Memo_TEMPLATE_v2.docx'
out = '/filesystem/Thelbridge_Verification_Memo_Item048_BlockB.docx'
doc = Document(src)

# Keep the supplied memorandum form and its section headings, replacing only form prompts.
texts = {
3: 'To:\tRachel Marlbeck, University Program Director, Thornbury State University',
4: 'From:\tA. Vance, Thelbridge Project Management Services',
5: 'Date:\t07/20/2026',
6: 'Subject:\tVerification Register Item 048 - Block B plant-room support of excavation, Submittal 31-SH-B Rev.1 as supplemented by Rev.2 (KE-L-2026-0713)',
8: ('Item 048 is the verification of Kesterline Engineering\'s Block B plant-room support-of-excavation design against the logged groundwater and subsurface conditions. '
    'This memorandum verifies the current design basis: Submittal 31-SH-B Rev.1 as modified by Kesterline\'s sealed Revision 2 Engineering Supplement, letter KE-L-2026-0713 dated 07/13/2026. '
    'The determination is limited to the temporary excavation support and groundwater-control design; it is not an approval of the permanent plant-room structure or a blanket release to excavate without the stated field hold points.'),
11: ('- Kesterline Engineering, Submittal 31-SH-B Rev.2, Revision 2 Engineering Supplement, letter KE-L-2026-0713, 07/13/2026, pp. 1-5 (sealed by Byron A. Halvard, PE).\n'
    '- Kesterline Engineering, Submittal 31-SH-B Rev.1, Block B Plant-Room Shoring Calculations, 06/11/2026, Sections 1-13.\n'
    '- Kelbrook Geotechnical, Geotechnical Investigation Report KGI-2024-0417 Rev.2, 02/14/2025, Sections 6-9, especially Sections 7.1, 7.2, 8.2, 9.4 and 9.6.\n'
    '- Kelbrook Geotechnical, Field Observation Report KGI-FO-2026-0528, 05/28/2026, Sections 2-4 and groundwater monitoring summary.\n'
    '- Boring Logs and Groundwater Monitoring B-01-B09, current project record.\n'
    '- Calloway Braddock, Design Basis Memorandum CB-DBM-001 Rev.2, 11/14/2025, Section 6.2.\n'
    '- Specification Section 31 20 00 Rev.3, Earth Moving and Support of Excavation requirements.\n'
    '- Sheet S-101 Foundation Plan Rev.4 and Sheet S-201 Foundation Sections and Details Rev.4.\n'
    '- Sheet A-501 Below-Grade Waterproofing Details Rev.3 and RFI 104 response.\n'
    '- Thelbridge Verification Register Package A, current through 07/15/2026, Item 048.\n'
    '- Rowan Bay Field Observation / Leak Report and Quote C4, 07/02/2026, and Pre-Pour Reinforcement Cover Inspection, 07/13/2026.'),
14: ('The review applied the current project record and the governing design criteria identified in the submittal. The recorded profile is: engineered fill / upper granular material to about El. 738.0; normally consolidated CL clay aquitard from El. 738.0 to El. 720.0; and dense SW-GW sand and gravel aquifer below El. 720.0. The logged shallow water table is El. 742.0 and the confined aquifer head is El. 738.0. The planned excavation runs from El. 750.0 to El. 726.0, leaving a 6.0 ft clay plug above the aquifer.\n\n'
    'Rev.1 was not carried forward as a dry-excavation design. Rev.2 expressly supersedes Rev.1 Sections 3.4, 4.3, 5, 6, 7, 9 and 10. Rev.1 Sections 1, 2, 3.1-3.3, 4.1, 4.2, 8, 11.3, 11.4, 12 and 13 remain in force. The governing review therefore uses the Rev.2 groundwater, base-heave, layered lateral-load, toe, anchor, flexure, deflection and instrumentation checks, together with the unchanged scope, surcharge, global stability, connection/detail and sequence provisions.\n\n'
    'The checks were tested for agreement with the logged elevations, soil parameters, groundwater record, design geometry and existing permanent-work drawings. This is a verification of the delegated design package, not a substitution for the Contractor\'s means-and-methods responsibility or the EOR\'s responsibility for the permanent work.'),
17: ('1. Groundwater and subsurface agreement. Rev.2 uses El. 742.0 for the shallow phreatic surface, El. 738.0 initial confined head, aquifer top at El. 720.0 and CL clay from El. 738.0 to El. 720.0. These values agree with GIR Rev.2 Sections 6-7, the boring/piezometer record, and the extended field report: shallow readings El. 741.6-742.4 and deep readings El. 737.7-738.3 through 05/2026. The reported 18 ft separation between the regimes remains applicable.\n\n'
    '2. Rev.2 groundwater control and staging. Four 8-in relief wells RW-B1 through RW-B4 are to be screened El. 718.0-705.0, sealed across the aquitard, and pumped to hold the confined head at or below El. 726.5. Three VW piezometers with tips at El. 719.0 are to verify the condition. Excavation below El. 732.0 requires a continuous 72-hour confirmation hold; a reading above El. 727.0 is a stop-work trigger, with pumping restored to El. 726.5 or lower before restart. This directly addresses GIR Rev.2 Section 9.4, which identified confined-aquifer uplift as the controlling constructability issue.\n\n'
    '3. Base-heave working. For the 6.0 ft clay plug, W = 6.0 x 120 = 720 psf; factored resistance = 0.90W = 648 psf. At controlled head El. 726.5, u = (726.5 - 720.0) x 62.4 = 405.6 psf. Therefore FS = 648 / 405.6 = 1.60, which exceeds the DBM Section 6.2 minimum of 1.50. The check is valid only while the controlled head is maintained and the plug is not disturbed.\n\n'
    '4. Lateral loading and wall checks. Rev.2 replaces the dry/blended pressure case below the water table with layered effective-stress plus hydrostatic loading. It reports 19,610 lb/ft horizontal load and 237,293 ft-lb/ft driving moment. The revised toe check uses 6.5 ft embedment to El. 719.5, net passive pressure 2,494 psf, resisting moment 368,800 ft-lb/ft and FS = 1.55 >= 1.50. The tieback demand is 56.2 kips at 6 ft spacing against 108.6 kips ultimate grout-bond capacity, FS = 1.93; proof test is 74.8 kips and lock-off is 42.2 kips. PZ-35 Grade 50 flexure is 62.4 kip-ft/ft against 121 kip-ft/ft allowable, FS = 1.94. Predicted wall deflection is 1.3 in against H/200 = 1.44 in.\n\n'
    '5. Checks carried forward as they stand. Rev.1 Sections 1, 2, 3.1-3.3, 4.1, 4.2, 8, 11.3, 11.4, 12 and 13 remain applicable, including project scope, codes, stratigraphy and soil parameters, 250 psf surcharge, global overturning/sliding checks, waler/bearing-plate/anchor-head details, and construction sequence notes/drawings. They are carried forward only as modified by the Rev.2 groundwater-control and revised analysis provisions.\n\n'
    '6. Checks not carried forward. Rev.1 Section 3.4 dry-excavation assumption, Section 4.3 pressure diagram, Section 5 base stability, Section 6 toe embedment, Section 7 anchor design, Section 9 sheet-pile flexure and Section 10 deflection/instrumentation are not valid on their own. They are superseded and cannot be used to release the work without the corresponding Rev.2 checks and field controls.\n\n'
    '7. Effect on permanent work already built. The planned cut within Block B (shown between grids H-L / 3-5 on S-101) reaches El. 726.0, approximately 5.5 ft below the standard basement-mat underside at El. 731.5 and 4.0 ft below the column-drop underside at El. 730.0. It therefore removes soil adjacent to and below portions of the completed Block B basement mat and may expose or pass alongside pile caps whose underside is El. 732.0 and whose piles continue to the deep bearing stratum. It also places temporary sheeting, anchors, drawdown and excavation-induced movement beside the completed mat, pile caps, basement wall and waterproofing/joint system. The shoring design is temporary and expressly does not design, underpin, or take credit for the permanent work. The Contractor must maintain the permanent-work support and waterproofing, avoid damage to reinforcement, pile caps, joints and drains, and obtain the EOR\'s written sequence/protection confirmation before cutting or loading near them. The C-4 seepage/crack record also means drainage and waterproofing protection must be monitored during the work; excavation is not a repair or authorization to disturb the existing basement system.\n\n'
    '8. Required before excavation. Rowan Bay, through its shoring/dewatering subcontractors, must produce: (a) installed and grouted RW-B1 through RW-B4 records, pump test/flow records and operating plan; (b) installed VW-B1 through VW-B3 calibration, baseline and continuous monitoring records; (c) the 72-hour readings confirming head at or below El. 726.5 before excavation below El. 732.0; (d) Kesterline/Contractor field confirmation of sheet-pile toe, sealed interlocks, tieback installation and proof tests at 74.8 kips, with lock-off records; (e) the final excavation sequence, emergency pumping/stop-work plan and instrumentation plan; and (f) a pre-excavation condition survey and protection/temporary-support plan for the existing mat, column drops, pile caps, piles, basement wall, waterproofing, joints, drains and the C-4 repair area. Kesterline must confirm the installed temporary works conform to Rev.2; Kelbrook must verify the groundwater readings and subgrade condition as the geotechnical consultant; and Calloway Braddock, as EOR, must confirm the protection and sequencing of the permanent work. Thelbridge is to witness/record the hold-point evidence before release.'),
20: ('Determination: VERIFIED WITH COMMENT for Item 048 on the basis of Submittal 31-SH-B Rev.1 as supplemented by sealed Rev.2, KE-L-2026-0713. The current design checks are consistent with the logged groundwater and subsurface conditions and the reported arithmetic satisfies the stated criteria. The Rev.1 dry-excavation case is not verified and is not a permissible basis for construction.\n\n'
    'Recommended register disposition: response by A. Vance, dated 07/20/2026: "Submittal 31-SH-B Rev.1 verified as supplemented by Kesterline Rev.2 Engineering Supplement, letter KE-L-2026-0713 dated 07/13/2026. Rev.2 groundwater-control, base-heave, layered lateral-load, toe, anchor, sheet-pile flexure and deflection checks verified against KGI-2024-0417 Rev.2, KGI-FO-2026-0528 and the Package A record. Rev.1 dry-excavation and superseded checks are not to be used. VERIFIED WITH COMMENT. Before excavation below El. 732.0, Rowan Bay shall complete the relief wells, VW piezometers and 72-hour head confirmation, install and proof-test the anchors, provide the temporary-work and permanent-work protection records, and obtain Kesterline, Kelbrook, EOR and Thelbridge hold-point confirmations. The 08/10/2026 planned start is feasible only if those conditions are satisfied and remains not released until the evidence is accepted."\n\n'
    'Status: Closed-w-Comment. The item may be closed because the current design has been verified, but the comment status preserves the mandatory field hold points and does not constitute an unconditional excavation release. If the listed evidence is not complete and accepted before 08/10/2026, the excavation must not start on that date and Item 048 must be reopened or the start deferred. No separate change to the permanent design is authorized by this memorandum.'),
23: 'A. Vance',
24: 'Project Engineer, Thelbridge Project Management Services',
26: '07/20/2026'
}
for i, text in texts.items():
    p = doc.paragraphs[i]
    p.text = text
    for run in p.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(9.5)
    if i in [3,4,5,6]:
        p.paragraph_format.space_after = Pt(2)
    elif i in [8,11,14,17,20]:
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.05

# Give headings a restrained, readable hierarchy while retaining their wording.
for i in [0,2,7,10,13,16,19]:
    p=doc.paragraphs[i]
    for r in p.runs:
        r.font.name='Arial'
        r.font.bold=True
        r.font.size=Pt(11 if i not in [0,2] else 13)
    p.paragraph_format.space_before=Pt(8 if i not in [0,2] else 2)
    p.paragraph_format.space_after=Pt(3)
for i in [1,25]:
    for r in doc.paragraphs[i].runs:
        r.font.name='Arial'; r.font.size=Pt(8)

# Set margins and default font.
for sec in doc.sections:
    sec.top_margin=Inches(0.55); sec.bottom_margin=Inches(0.55)
    sec.left_margin=Inches(0.7); sec.right_margin=Inches(0.7)

# Add page numbers in the footer without changing the supplied form structure.
sec=doc.sections[0]
footer=sec.footer.paragraphs[0]
footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=footer.add_run('Page ')
r.font.name='Arial'; r.font.size=Pt(8)
fldChar1=OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'),'begin')
instr=OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text='PAGE'
fldChar2=OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'),'end')
r._r.append(fldChar1); r._r.append(instr); r._r.append(fldChar2)

doc.save(out)
print(out)
