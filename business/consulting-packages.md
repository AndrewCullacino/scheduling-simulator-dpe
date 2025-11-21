# PySchedule Consulting Packages

## Overview

PySchedule offers tiered consulting packages designed to address different customer needs and budgets. Each package is structured based on validated customer discovery insights (see [Customer Discovery Log](./customer-discovery-log.md)) and proven implementation patterns.

**Core Consulting Philosophy**:
- **Speed-to-value**: Deliver measurable results in 4-8 weeks, not months
- **Risk mitigation**: Pilot approach before full commitment
- **Transparent methodology**: Simulation-based analysis with clear visualizations
- **Knowledge transfer**: Train client teams for ongoing optimization

---

## Package Comparison Matrix

| Feature | Pilot | Standard | Enterprise | Retainer |
|---------|-------|----------|------------|----------|
| **Price** | $15,000 | $30,000 | $50,000-80,000 | $5,000-10,000/month |
| **Duration** | 4 weeks | 8 weeks | 10-12 weeks | Ongoing |
| **Team Size** | 1 consultant | 1-2 consultants | 2-3 consultants | Flexible |
| **Scope** | Single scenario | Full implementation | Multi-facility/custom | Continuous optimization |
| **Deliverables** | Analysis + recommendations | Implementation + training | Custom algorithms + deployment | Monthly optimization reports |
| **Best For** | Proof-of-value | Standard deployment | Complex R&D needs | Long-term partnership |

---

## Package 1: Pilot Package

### Overview
**Price**: $15,000
**Duration**: 4 weeks
**Target Audience**: Companies seeking fast proof-of-value before larger commitment

**Customer Jobs Addressed** (from customer discovery):
- Cloud infrastructure: "Show me 20% cost savings in 4-6 weeks"
- Manufacturing: "Prove this works for my shop before I commit"
- Risk-averse buyers: "I need to see results before investing more"

---

### Scope of Work

#### Week 1: Discovery & Data Collection
**Objectives**:
- Understand current scheduling approach and pain points
- Gather representative workload data
- Identify quick-win optimization opportunities

**Activities**:
- Kickoff meeting (2 hours): Scope definition, stakeholder alignment
- Data collection: Historical workload traces, infrastructure topology
- Pain point interviews: 3-5 key stakeholders (DevOps, operations managers)
- Current state documentation: Baseline metrics, scheduling policies

**Deliverables**:
- Current state analysis report (10-15 pages)
- Data quality assessment
- Preliminary bottleneck identification

---

#### Week 2: Simulation & Analysis
**Objectives**:
- Build simulation model of current scheduling approach
- Test alternative algorithms (SPT, EDF, DPE variants)
- Quantify improvement opportunities

**Activities**:
- Scenario generation from real workload data
- Baseline simulation (current scheduling approach)
- Algorithm comparison experiments
- Sensitivity analysis (α parameters for DPE)

**Deliverables**:
- Simulation results report (15-20 pages)
- Gantt chart visualizations (before/after comparisons)
- Performance metrics comparison table
- Algorithm recommendation with rationale

**Tools Used**:
- PySchedule simulation framework
- Custom scenario generation from client data
- Matplotlib/Seaborn for visualizations

---

#### Week 3: Recommendation Development
**Objectives**:
- Develop actionable recommendations
- Create implementation roadmap
- Estimate expected ROI

**Activities**:
- Recommendation synthesis meeting
- Implementation feasibility assessment
- Risk analysis and mitigation planning
- ROI calculation (cost savings, efficiency gains)

**Deliverables**:
- Executive summary (2-3 pages)
- Detailed recommendations report (20-25 pages)
- Implementation roadmap (phases, timeline, resources)
- ROI projection (conservative, expected, optimistic scenarios)

---

#### Week 4: Presentation & Knowledge Transfer
**Objectives**:
- Present findings to stakeholders
- Answer questions and address concerns
- Provide next-step options

**Activities**:
- Executive presentation (1-2 hours)
- Technical deep-dive session (2-3 hours)
- Q&A and recommendation refinement
- Handoff documentation delivery

**Deliverables**:
- Executive presentation (20-30 slides)
- Technical documentation package
- Next-step options (expand to Standard Package, implement independently)
- 2 weeks post-engagement support (email/Slack)

---

### Investment & ROI

**Investment**: $15,000 (4 weeks)

**Expected Outcomes**:
- Quantified improvement opportunity (typically 15-35% efficiency gains)
- Clear implementation roadmap
- Risk assessment and mitigation plan
- Foundation for Standard Package (if client proceeds)

**Typical ROI Scenarios** (based on customer discovery):
- **Cloud Infrastructure** (500-container deployment):
  - Baseline: $50K/month infrastructure spend
  - Expected savings: 20% = $10K/month = $120K/year
  - Pilot ROI: 8x annual return

- **Manufacturing SMB** (50-machine shop):
  - Baseline: 15% capacity underutilization = $200K/year opportunity cost
  - Expected recovery: 10% capacity = $133K/year revenue gain
  - Pilot ROI: 9x annual return

**Decision Point After Pilot**:
- **Option A**: Proceed to Standard Package ($30K) for full implementation
- **Option B**: Implement recommendations independently
- **Option C**: Pause (client retains all analysis and recommendations)

---

## Package 2: Standard Implementation Package

### Overview
**Price**: $30,000
**Duration**: 8 weeks
**Target Audience**: Companies ready for full implementation after proof-of-value

**Customer Jobs Addressed**:
- "I need someone to implement this for me, not just tell me what to do"
- "I want ongoing support during rollout"
- "I need my team trained so we can maintain this"

---

### Scope of Work

#### Phase 1: Foundation (Weeks 1-2)
Same as Pilot Package Weeks 1-2, but with:
- **Deeper data collection**: 6-12 months historical data
- **More comprehensive interviews**: 5-10 stakeholders
- **Production system integration planning**: API design, deployment architecture

---

#### Phase 2: Implementation (Weeks 3-5)

**Week 3: Integration Architecture**
**Objectives**:
- Design production integration approach
- Set up monitoring and alerting
- Plan gradual rollout strategy

**Activities**:
- API design for scheduler integration
- Monitoring dashboard setup (Prometheus, Grafana, CloudWatch)
- Staging environment configuration
- Rollout plan (pilot subset → gradual expansion → full deployment)

**Deliverables**:
- Integration architecture document
- API specifications (RESTful or gRPC)
- Monitoring setup guide
- Rollout timeline and success criteria

---

**Week 4: Pilot Deployment**
**Objectives**:
- Deploy to pilot subset (10-20% of workload)
- Monitor performance and gather feedback
- Iterate on configuration

**Activities**:
- Pilot scheduler deployment
- Real-time monitoring and alerting setup
- Performance comparison (baseline vs. new scheduler)
- Issue triage and resolution

**Deliverables**:
- Pilot deployment report
- Performance metrics (before/after comparison)
- Issue log and resolutions
- Configuration refinements

---

**Week 5: Full Deployment**
**Objectives**:
- Expand to full production workload
- Validate performance at scale
- Optimize parameters based on production data

**Activities**:
- Gradual rollout to 100% of workload
- Continuous performance monitoring
- Parameter tuning (α adjustment for DPE)
- Stakeholder communication and updates

**Deliverables**:
- Full deployment report
- Production performance dashboard
- Optimized configuration files
- Incident response playbook

---

#### Phase 3: Knowledge Transfer & Handoff (Weeks 6-8)

**Week 6: Team Training**
**Objectives**:
- Train client team on ongoing optimization
- Document troubleshooting procedures
- Establish maintenance processes

**Activities**:
- Training workshop (full-day, hands-on)
- Troubleshooting guide review
- Runbook creation (common scenarios)
- Handoff of simulation tools and code

**Deliverables**:
- Training materials (slides, exercises, recordings)
- Troubleshooting guide
- Operations runbook
- Source code and simulation scenarios

---

**Week 7: Validation & Optimization**
**Objectives**:
- Validate production performance matches projections
- Fine-tune based on 2-3 weeks real-world data
- Address any edge cases or anomalies

**Activities**:
- Performance review meeting
- Edge case analysis and mitigation
- Final parameter optimization
- Documentation updates

**Deliverables**:
- Validation report (projected vs. actual results)
- Edge case documentation
- Final optimized configuration
- Updated technical documentation

---

**Week 8: Wrap-Up & Future Planning**
**Objectives**:
- Conduct project retrospective
- Document lessons learned
- Plan future optimization opportunities

**Activities**:
- Final executive presentation
- Retrospective meeting (what worked, what to improve)
- Future roadmap discussion
- Case study development (if client permits)

**Deliverables**:
- Final project report
- Lessons learned document
- Future optimization roadmap
- Case study (if approved)

---

### Investment & ROI

**Investment**: $30,000 (8 weeks)

**Expected Outcomes**:
- Fully deployed production scheduling system
- Trained internal team
- Measurable performance improvements
- Ongoing optimization capabilities

**Typical ROI Scenarios**:
- **Cloud Infrastructure**:
  - Implementation: $30K
  - Annual savings: $120K-240K (20-40% infrastructure cost reduction)
  - ROI: 4-8x annual return
  - Payback period: 1.5-3 months

- **Manufacturing**:
  - Implementation: $30K
  - Annual value: $150K-300K (10-20% capacity recovery)
  - ROI: 5-10x annual return
  - Payback period: 1.2-2.4 months

**Support Period**: 4 weeks post-engagement email/Slack support included

---

## Package 3: Enterprise Custom Package

### Overview
**Price**: $50,000-80,000 (customized based on scope)
**Duration**: 10-12 weeks
**Target Audience**: Large enterprises, multi-facility deployments, custom R&D needs

**Customer Jobs Addressed**:
- "We need custom algorithms for our unique constraints"
- "We have 5 facilities that need coordinated scheduling"
- "We want to co-develop novel scheduling approaches"

---

### Scope of Work (Customizable)

#### Core Components (All Enterprise Engagements)

**Discovery & Architecture (Weeks 1-3)**:
- Comprehensive stakeholder interviews (10-20 people)
- Multi-facility data collection and analysis
- Enterprise integration architecture (SSO, RBAC, audit logging)
- Security review and compliance assessment (SOC 2, HIPAA if applicable)

**Custom Algorithm Development (Weeks 4-7)**:
- Requirements analysis for custom scheduling logic
- Algorithm design and theoretical analysis
- Implementation and unit testing
- Validation against synthetic and real workload traces

**Multi-Facility Deployment (Weeks 8-11)**:
- Phased rollout across facilities
- Facility-specific configuration and optimization
- Cross-facility coordination mechanisms (if needed)
- Performance monitoring and alerting at scale

**Knowledge Transfer & Support (Week 12)**:
- Comprehensive training program (2-3 days)
- Executive presentation and ROI documentation
- Handoff of all code, documentation, and tools
- 8 weeks post-engagement support

---

#### Optional Add-Ons

**Research Collaboration** (+$15,000-30,000):
- Co-author academic paper on novel algorithms
- Conference presentation preparation
- Patent filing support (if applicable)

**Advanced Monitoring & Alerting** (+$10,000):
- Custom Grafana dashboards
- Predictive anomaly detection
- Automated reporting and insights

**Ongoing Optimization Services**:
- Transition to Retainer Package (see below)

---

### Investment & ROI

**Investment**: $50,000-80,000 (10-12 weeks)

**Expected Outcomes**:
- Custom scheduling algorithms tailored to unique constraints
- Multi-facility deployment and coordination
- Enterprise-grade security and compliance
- Potential for competitive advantage through novel approaches

**Typical ROI Scenarios**:
- **Large Cloud Provider** (10,000+ containers):
  - Implementation: $70K
  - Annual savings: $500K-1M (20-30% infrastructure optimization)
  - ROI: 7-14x annual return
  - Additional value: Competitive differentiation, patent potential

- **Multi-Facility Manufacturer** (200+ machines across 5 sites):
  - Implementation: $60K
  - Annual value: $400K-800K (15-25% capacity recovery)
  - ROI: 7-13x annual return
  - Additional value: Coordinated production planning

**Support Period**: 8 weeks post-engagement with dedicated support channel

---

## Package 4: Retainer - Continuous Optimization

### Overview
**Price**: $5,000-10,000/month (minimum 6-month commitment)
**Target Audience**: Existing clients seeking ongoing optimization and strategic partnership

**Customer Jobs Addressed**:
- "Our workload changes seasonally; we need ongoing tuning"
- "We want to stay ahead of competitors with continuous improvements"
- "We value having an expert on-call for scheduling questions"

---

### Retainer Services

#### Monthly Deliverables

**Performance Monitoring & Reporting**:
- Monthly performance dashboard review
- KPI tracking (cost savings, utilization, tardiness, fairness)
- Trend analysis and anomaly detection
- Executive summary report (2-3 pages)

**Continuous Optimization**:
- Parameter tuning based on workload evolution
- New scenario development for changing use cases
- Algorithm refinement for edge cases
- A/B testing new scheduling policies

**Strategic Consulting**:
- Quarterly strategy sessions (2 hours)
- Roadmap planning for future enhancements
- Industry trend analysis and recommendations
- Competitive benchmarking

**Priority Support**:
- Dedicated Slack channel (4-hour response time)
- Emergency support for production issues
- Ad-hoc analysis requests (up to 8 hours/month)

---

#### Retainer Tiers

**Standard Retainer**: $5,000/month
- Monthly performance reports
- Quarterly optimization cycles
- Email/Slack support (24-hour response)
- 8 hours/month ad-hoc consulting

**Premium Retainer**: $7,500/month
- All Standard features
- Bi-weekly performance reviews
- Monthly optimization cycles
- Priority Slack support (4-hour response)
- 16 hours/month ad-hoc consulting

**Enterprise Retainer**: $10,000/month
- All Premium features
- Weekly performance reviews
- Continuous optimization (not monthly batches)
- 2-hour emergency response SLA
- 24 hours/month ad-hoc consulting
- Dedicated account manager

---

### Investment & ROI

**Investment**: $5,000-10,000/month ($60,000-120,000/year)

**Expected Outcomes**:
- Sustained performance improvements (prevents regression)
- Adaptation to changing workload patterns
- Continuous competitive advantage
- Reduced internal staffing needs for optimization

**Typical ROI Scenarios**:
- **Cloud Infrastructure** (sustained $150K/year savings):
  - Retainer: $60K/year
  - Net benefit: $90K/year
  - ROI: 2.5x ongoing return
  - Value-add: Prevents regression, adapts to growth

- **Manufacturing** (sustained $200K/year value):
  - Retainer: $75K/year
  - Net benefit: $125K/year
  - ROI: 2.7x ongoing return
  - Value-add: Seasonal optimization, new product introduction support

---

## Cross-Selling & Upselling Paths

### Typical Customer Journey

**Stage 1: Pilot Package** ($15K)
- Risk-free proof-of-value
- 85% of pilots proceed to Standard Package (based on projected conversions)

**Stage 2: Standard Package** ($30K)
- Full implementation and training
- 40% of Standard clients add Retainer within 6 months

**Stage 3: Retainer** ($60-120K/year)
- Ongoing partnership
- 15% of Retainer clients expand to Enterprise for new facilities/projects

**Stage 4: Enterprise Expansion** ($50-80K)
- Custom R&D, multi-facility deployments
- Long-term strategic partnership

---

### Package Bundles & Discounts

**Pilot-to-Standard Fast Track**: $40,000 (save $5K)
- Commit to Standard Package upfront
- Pilot integrated into Weeks 1-2 of Standard
- Faster time-to-deployment

**Standard + 6-Month Retainer**: $55,000 first year
- $30K Standard + $30K Retainer (6 months @ $5K) = $60K
- Bundle discount: $5K savings
- Ensures sustained value capture

**Enterprise + Annual Retainer**: $115,000 first year
- $70K Enterprise + $60K Retainer (12 months @ $5K) = $130K
- Bundle discount: $15K savings
- Strategic partnership commitment

---

## Terms & Conditions

### Payment Terms

**Pilot Package**:
- 50% upfront ($7,500)
- 50% upon delivery of final report ($7,500)

**Standard Package**:
- 40% upfront ($12,000)
- 40% at Week 5 deployment milestone ($12,000)
- 20% upon project completion ($6,000)

**Enterprise Package**:
- 30% upfront (${amount})
- 40% at Week 6 custom algorithm delivery (${amount})
- 30% upon project completion (${amount})

**Retainer**:
- Monthly invoicing, payment due within 15 days
- 6-month minimum commitment
- 30-day cancellation notice after minimum term

---

### Cancellation & Refund Policy

**Pilot Package**:
- Cancel within 5 business days: Full refund minus $1,000 setup fee
- Cancel after Week 1: 50% refund
- Cancel after Week 2: No refund (work substantially complete)

**Standard & Enterprise**:
- Cancel before Week 3: Refund of unworked milestones minus 20% administrative fee
- Cancel after Week 5 (Standard) or Week 7 (Enterprise): No refund

**Retainer**:
- Cancel with 30-day notice after minimum 6-month term
- Pro-rated refund if paid quarterly/annually

---

### Intellectual Property

**Client Retains**:
- All custom code developed specifically for client use cases
- All simulation models based on client proprietary data
- All analysis reports and recommendations

**PySchedule Retains**:
- Core PySchedule framework (open-source MIT license)
- Generalized algorithms and patterns (for future client benefit)
- Right to anonymized case study (with client approval)

**Shared IP**:
- Novel algorithms co-developed may be co-owned
- Publication rights negotiated case-by-case
- Patent filing costs shared if jointly pursued

---

## Success Metrics & Guarantees

### Performance Guarantees

**Pilot Package**:
- Deliver quantified recommendations within 4 weeks
- If analysis shows <10% improvement opportunity, 50% refund

**Standard Package**:
- Deploy production system within 8 weeks
- Achieve at least 50% of projected efficiency gains within 4 weeks of deployment
- If <25% of projections achieved, continue work at no additional cost until met

**Enterprise Package**:
- Custom algorithm performance meets specifications
- Multi-facility deployment completed on schedule
- Customized guarantees negotiated per engagement

**Retainer**:
- Monthly reports delivered on time
- Response SLAs met 95%+ of the time
- Performance maintained or improved year-over-year

---

## Client Responsibilities

### Data Access & Availability
- Provide access to historical workload data (6-12 months preferred)
- Grant API access for monitoring and integration (Standard/Enterprise)
- Ensure stakeholder availability for interviews and meetings

### Infrastructure & Resources
- Provide staging environment for testing (Standard/Enterprise)
- Allocate internal engineering support (4-8 hours/week)
- Ensure necessary approvals for production deployment

### Communication & Feedback
- Designate primary point of contact
- Provide timely feedback on deliverables (48-hour turnaround)
- Attend scheduled check-in meetings

---

## Getting Started

### Onboarding Process

**Step 1: Initial Consultation** (30-60 minutes, free)
- Understand your scheduling challenges
- Assess fit for PySchedule approach
- Recommend appropriate package

**Step 2: Proposal & SOW**
- Detailed scope of work document
- Timeline and deliverables
- Pricing and payment terms

**Step 3: Contract Execution**
- Review and sign consulting agreement
- Submit initial payment
- Schedule kickoff meeting

**Step 4: Kickoff** (Week 1, Day 1)
- Meet full project team
- Review scope and expectations
- Begin discovery activities

---

### Contact & Next Steps

**Ready to get started?**
- Schedule consultation: [Calendly link placeholder]
- Email: pyschedule@example.com
- Questions: See [FAQ](./faq.md) or book a call

**Resources**:
- [Customer Discovery Log](./customer-discovery-log.md) - Validated customer insights
- [Case Study Template](./case-study-template.md) - Engagement documentation approach
- [Market Analysis](./market-analysis.md) - Market opportunity and customer segments

---

**Version**: 1.0
**Last Updated**: 2024-11
**Author**: PySchedule Development Team

**Note**: Pricing and terms are subject to change. Contact us for current offerings and custom enterprise pricing.
