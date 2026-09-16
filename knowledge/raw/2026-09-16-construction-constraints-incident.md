# Construction constraints incident — supplied retrospective excerpt

Received from the maintainer on 2026-09-16 with a request to turn the incident into durable,
generic workflow knowledge. The following excerpts are from the supplied agent retrospective;
the consuming project's code, approvals and execution history were not independently inspected.
Omissions are indicated by separate quotations. Product-specific names are retained only in this
source; the derived concept generalizes the lesson.

> Yes. Your instruction was explicit:
>
> 1. Finish and approve the Opportunity experience first.
> 2. Turn its board canvas and page structure into reusable components.
> 3. Build Processos by composing those components with process-specific data and actions.
>
> I did not follow it.

> But it is not the cause here: the compacted summary still contained your instruction that Opportunity should be improved first and then reused for Processos. I had enough
> information to make the correct decision.

> - I treated “reuse the Opportunity structure” as a visual requirement instead of a code-architecture requirement.
> - The Process workflow contract described process behavior thoroughly but did not make shared Opportunity components a blocking acceptance criterion.
> - I dispatched Processos as an independent implementation slice.
> - The implementer was given ownership of process-board.tsx and optimized within that boundary.
> - Visual remediation then focused on making the duplicate resemble Opportunity.
> - Verification checked behavior, layout, and criteria. It did not require both pages to import the same board canvas.
> - I accepted passing tests and improving screenshots without checking whether the implementation followed your required construction sequence.
> - I allowed Processos work to begin before receiving your final approval of the reusable Opportunity implementation.

> So the honest answer is: compaction was a risk, but it did not erase your instruction. I made the wrong planning decision and then used verification that could not detect the architectural violation.
