# Part 2 R3: Exact Lift-Digit Law and State-Space Audit

## Status

This note advances the repaired Part 2 program from the compatible-residue theorem to the exact next-lift formula. It also records a decisive limitation:

\[
\boxed{\text{The shell split alone does not yield a finite-state lift automaton.}}
\]

A finite quotient may still exist, but it requires a separate theorem.

---

## 1. Valid prefix data

For an affine block sequence
\[
2^{m_i}y_i=3^{s_i}y_{i-1}+D_i,
\qquad m_i\ge1,
\]
put
\[
M_n=\sum_{i\le n}m_i,
\qquad
S_n=\sum_{i\le n}s_i,
\]
and define the exact prefix cocycle
\[
2^{M_n}y_n=3^{S_n}y_0+C_n,
\]
where
\[
C_{n+1}=3^{s_{n+1}}C_n+2^{M_n}D_{n+1}.
\]

Define the 2-adic prefix target
\[
z_n:=-3^{-S_n}C_n\in\mathbb Z_2.
\]
Then
\[
z_n\equiv r_n\pmod{2^{M_n}},
\]
where \(r_n\) is the compatible residue class for the starting parameter. Let
\[
a_n\in\{0,1,\dots,2^{M_n}-1\}
\]
be its canonical representative.

---

## 2. Exact lift-digit formula

Let
\[
u_{n+1}:=3^{-S_{n+1}}D_{n+1}\in\mathbb Z_2.
\]
The cocycle recurrence gives the **exact** 2-adic relation
\[
\boxed{
z_{n+1}=z_n-2^{M_n}\nu_{n+1}.
}
\]

Write
\[
z_n=a_n+2^{M_n}\lambda_n,
\qquad \lambda_n\in\mathbb Z_2.
\]
Then
\[
z_{n+1}=a_n+2^{M_n}(\lambda_n-\nu_{n+1}).
\]

Since \(M_{n+1}=M_n+m_{n+1}\), the next canonical representative has the form
\[
a_{n+1}=a_n+2^{M_n}b_n,
\qquad 0\le b_n<2^{m_{n+1}},
\]
with
\[
\boxed{
b_n\equiv\lambda_n-\nu_{n+1}\pmod{2^{m_{n+1}}}.
}
\tag{L}
\]

Hence the exact criterion for a zero lift digit is
\[
\boxed{
b_n=0
\iff
\lambda_n\equiv3^{-S_{n+1}}D_{n+1}\pmod{2^{m_{n+1}}}.
}
\tag{Z}
\]

This is the correct replacement for the invalid claim that every lift is automatically nonzero or odd.

---

## 3. Why oddness is insufficient

Oddness of \(D_{n+1}\) implies only that \(\nu_{n+1}\) is a 2-adic unit. But formula (L) compares that unit with the existing higher lift \(\lambda_n\). The latter is unconstrained by the residue modulo \(2^{M_n}\).

Thus neither of the following follows from \(D_{n+1}\) odd:
\[
b_n\ne0,
\qquad
v_2(a_{n+1}-a_n)=M_n.
\]

The generic fixed example
\[
2\cdot1=3\cdot1-1
\]
realizes \(b_n=0\) at every level.

Even positivity and a lower bound on \(m\) do not repair the generic argument. For example,
\[
2^3\cdot1=3\cdot1+5
\]
has \(m=3\), \(D=5>0\), and stabilizing starting parameter \(y=1\).

Therefore any recovery must use restrictions specific to the genuine Collatz block language.

---

## 4. Genuine Part 2 block alphabet is infinite

The manuscript's actual blocks have parameter families:

### Return block
\[
m=b+2d,
\qquad s=b+d,
\qquad D=3^{d-1}(3^b-2^b),
\]
subject to valuation conditions generated from
\[
3t+1=2^b u,
\qquad 3^bu-1=2^{2d}v.
\]

### Exit-plus-staircase block

For \(c=2h\):
\[
m=e+a'+2h,
\qquad s=a'+h-1,
\qquad D=3^{h-1}D_{e,a'}.
\]

For \(c=2h-1\):
\[
m=e+a'+2h-1,
\qquad s=a'+h-1,
\qquad D=3^{h-1}D_{e,a'}.
\]

Here \(b,d,e,a',h\) are unbounded positive parameters, constrained by higher 2-adic valuations of the evolving shell parameter.

Consequently, the raw transition alphabet is infinite. A statement such as
\[
(\text{shell type},\text{block type})\mapsto b_n
\]
is not a finite-state automaton merely because there are two named shells.

---

## 5. The finite-state gate

Formula (L) shows that calculating \(b_n\) requires
\[
\lambda_n\pmod{2^{m_{n+1}}}.
\]
Equivalently, it requires \(z_n\) modulo the stronger modulus
\[
2^{M_n+m_{n+1}}.
\]

Thus a finite-state reduction needs a theorem of the following form:

\[
\boxed{
\begin{minipage}{0.85\linewidth}
There exists a finite quotient state \(\sigma_n\) of the actual Collatz return/exit data such that both the legal next block and the residue of \(\lambda_n\) modulo \(2^{m_{n+1}}\) are determined by \(\sigma_n\).
\end{minipage}
}
\tag{FQ}
\]

No such theorem appears in Part 2, and it does not follow from Propositions 3.1--5.2.

---

## 6. Recovery consequences

The current status is:

\[
\text{compatible-residue theorem} \quad [██████████]\ 100\%
\]
\[
\text{exact lift-digit law (L)} \quad [██████████]\ 100\%
\]
\[
\text{finite quotient theorem (FQ)} \quad [░░░░░░░░░░]\ 0\%
\]
\[
\text{exclude eventual-zero lift tails} \quad [░░░░░░░░░░]\ 0\%
\]
\[
\text{no-divergence theorem} \quad [░░░░░░░░░░]\ 0\%
\]

The immediate research question is not yet whether every \(b_n\) is nonzero. It is whether the genuine return/exit valuation constraints provide a finite quotient satisfying (FQ), or whether they retain unbounded 2-adic memory. The answer determines whether the automaton route is viable.

---

## 7. Next falsifiable experiment

For a bounded range of true Collatz orbit prefixes:

1. extract each actual return/exit block and all valuation parameters;
2. calculate \(\lambda_n\bmod 2^{m_{n+1}}\) and \(b_n\) exactly;
3. group prefixes by candidate finite state (shell, low residues, valuation tuple truncated at a fixed depth);
4. look for two prefixes with the same candidate state but different next \(b_n\).

A collision of that kind disproves the candidate quotient. A lack of collisions is only a lead; it does not prove (FQ).

No global conclusion about Collatz is made in this note.