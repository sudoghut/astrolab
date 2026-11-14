/-
Environment-level audit of a study's `Argument` module (design/007 section 2.2, step 3).

Run inside the built Lake project:  lake env lean Audit.lean
This file does NOT `import Argument`: it loads the compiled module at runtime, so macros or
notation defined in Argument.lean cannot rewrite the checks below. Output lines:
  PREMISE <name> | prov=<p> | head=<h> | literal=<b> | proj=<b> | num=<op>:<value>|none | forbidden=<names> | body=<lean> | doc=<text>
  CONCLUSION | head=<h> | literal=<b> | proj=<b> | forbidden=<names> | body=<lean> | doc=<text>
  ERROR: <message>
and finally exactly one of AUDIT_OK / AUDIT_FAILED.
-/
import Lean
open Lean Meta Elab

def ns : Name := `Argument
def A (s : String) : Name := ns.str s
def vocabN : Name := A "Vocab"

/-- Constants allowed inside `prem` arms and `Conclusion`, besides `Vocab` projections. -/
def allowedConsts : List Name :=
  [``Not, ``And, ``Or, ``Iff, ``Exists, ``True, ``False, ``Eq, ``Ne,
   ``LE.le, ``LT.lt, ``GE.ge, ``GT.gt, ``OfNat.ofNat, ``Neg.neg, ``Nat, ``Int,
   ``instOfNatNat, ``instOfNat, ``instLENat, ``instLTNat,
   ``Int.instLEInt, ``Int.instLTInt, ``Int.instNegInt]

def relOps : List (Name × String) :=
  [(``GE.ge, ">="), (``GT.gt, ">"), (``LE.le, "<="), (``LT.lt, "<"), (``Eq, "==")]

def flipOp : String → String
  | ">=" => "<=" | "<=" => ">=" | ">" => "<" | "<" => ">" | o => o

structure Ctx where
  projs : List Name

def isProjApp (c : Ctx) (e : Expr) : Bool :=
  match e.getAppFn with
  | .const n _ => c.projs.contains n
  | _ => false

/-- Integer literal value of `OfNat.ofNat _ n _` or `Neg.neg _ _ (OfNat.ofNat _ n _)`. -/
partial def litVal? (e : Expr) : Option Int :=
  let e := e.consumeMData
  if e.isAppOfArity ``OfNat.ofNat 3 then
    match e.appArg!.consumeMData, (e.getArg! 1).consumeMData with
    | _, .lit (.natVal n) => some n
    | _, _ => none
  else if e.isAppOfArity ``Neg.neg 3 then
    (litVal? e.appArg!).map (fun v => -v)
  else none

/-- Relation `a op b` with its operator string, if `e` is one of the comparison constants. -/
def relParts? (e : Expr) : Option (String × Expr × Expr) :=
  let e := e.consumeMData
  match e.getAppFn with
  | .const n _ =>
    match relOps.lookup n with
    | some op =>
      let args := e.getAppArgs
      if args.size ≥ 2 then some (op, args[args.size - 2]!, args[args.size - 1]!) else none
    | none => none
  | _ => none

/-- `p → False` is read as `¬ p`. -/
def asNot? (e : Expr) : Option Expr :=
  let e := e.consumeMData
  if e.isAppOfArity ``Not 1 then some e.appArg!
  else match e with
    | .forallE _ d b _ => if !b.hasLooseBVars && b.consumeMData.isConstOf ``False then some d else none
    | _ => none

def headOf (e : Expr) : String :=
  let e := e.consumeMData
  match asNot? e with
  | some _ => "not"
  | none =>
    match e with
    | .forallE _ _ b _ => if b.hasLooseBVars then "forall" else "imp"
    | _ =>
      if e.isAppOf ``And then "and" else if e.isAppOf ``Or then "or"
      else if e.isAppOf ``Iff then "iff" else if e.isAppOf ``Exists then "exists"
      else if (relParts? e).isSome || e.isAppOf ``Ne then "rel" else "atom"

/-- Type argument of a comparison (`@LE.le α _ a b`, `@Eq α a b`, `@Ne α a b`). -/
def relType? (e : Expr) : Option Expr :=
  let args := e.consumeMData.getAppArgs
  if args.size ≥ 3 then some args[0]!.consumeMData else none

def isNumType (t : Expr) : Bool := t.isConstOf ``Nat || t.isConstOf ``Int

/-- Operands of `a ≠ b`. -/
def neParts? (e : Expr) : Option (Expr × Expr) :=
  let e := e.consumeMData
  if e.isAppOfArity ``Ne 3 then some (e.getArg! 1, e.getArg! 2) else none

def isNumOperand (c : Ctx) (e : Expr) : Bool :=
  let e := e.consumeMData
  isProjApp c e || e.isFVar || e.isBVar

/-- Literal relation: a Nat/Int field (or bound variable) compared with an integer literal. -/
def isLiteralRel (c : Ctx) (e : Expr) : Bool :=
  let ops : Option (Expr × Expr) := match relParts? e with
    | some (_, a, b) => some (a, b)
    | none => neParts? e
  match ops, relType? e with
  | some (a, b), some ty =>
    isNumType ty && ((isNumOperand c a && (litVal? b).isSome) || (isNumOperand c b && (litVal? a).isSome))
  | _, _ => false

/-- Atom: a Prop field, or a predicate field applied to arguments; never an equality of Props. -/
def isAtom (c : Ctx) (e : Expr) : Bool := isProjApp c e.consumeMData

def isAtomOrRel (c : Ctx) (e : Expr) : Bool :=
  isAtom c e || isLiteralRel c e

def isLiteral (c : Ctx) (e : Expr) : Bool :=
  match asNot? e with
  | some a => isAtomOrRel c a
  | none => isAtomOrRel c e

/-- `field op literal`, normalised to field-on-left. -/
def numForm? (c : Ctx) (e : Expr) : Option (String × Int) :=
  match relParts? e with
  | some (op, a, b) =>
    if isProjApp c a then (litVal? b).map (fun v => (op, v))
    else if isProjApp c b then (litVal? a).map (fun v => (flipOp op, v))
    else none
  | none => none

def constsOf (e : Expr) : List Name := e.getUsedConstants.toList

/-- Unfold `prem`'s own matcher (and any `match_*` auxiliary) at the head, then iota/beta. -/
partial def reduceMatch (e : Expr) : MetaM Expr := do
  let e ← whnfCore e
  match e.getAppFn with
  | .const n _ =>
    let last := match n with | .str _ s => s | _ => ""
    if last.startsWith "match_" then
      match ← unfoldDefinition? e with
      | some e' => reduceMatch e'
      | none => pure e
    else pure e
  | _ => pure e

def oneLine (s : String) : String := (s.replace "\n" " ").replace "\r" " "

def elabStr (s : String) : TermElabM Expr := do
  match Parser.runParserCategory (← getEnv) `term s with
  | .error err => throwError "cannot parse pinned statement '{s}': {err}"
  | .ok stx =>
    let e ← Term.elabTerm stx none
    Term.synthesizeSyntheticMVarsNoPostponing
    instantiateMVars e

def audit : TermElabM (Array String) := do
  let env ← getEnv
  let errs ← IO.mkRef (#[] : Array String)
  let err (m : String) : TermElabM Unit := errs.modify (·.push m)
  let some idx := env.getModuleIdx? ns | return #["module Argument not found"]
  let names := env.header.moduleData[idx.toNat]!.constNames
  -- 1. axioms of every constant; no meta/IO-typed declarations
  let allowedAx := [``propext, ``Quot.sound, ``Classical.choice]
  for n in names do
    if n.isInternal then continue
    for a in (← collectAxioms n) do
      unless allowedAx.contains a do err s!"{n} depends on non-whitelisted axiom {a}"
    let some ci := env.find? n | continue
    let bad (c : Name) : Bool := c.getRoot == `Lean || c == ``IO || c == ``EIO || c == ``BaseIO
    if (constsOf ci.type).any bad then err s!"declaration with meta/IO type: {n}"
    if let .defnInfo d := ci then
      if (constsOf d.value).any bad then err s!"definition with meta/IO value: {n}"
  -- 2. fixed block A: Prov
  match env.find? (A "Prov") with
  | some (.inductInfo pi) =>
    let want := [A "Prov" |>.str "stated", A "Prov" |>.str "implied", A "Prov" |>.str "reconstructed"]
    if pi.numParams != 0 || pi.numIndices != 0 || pi.ctors != want then
      err "Prov must be exactly: inductive Prov | stated | implied | reconstructed"
  | _ => err "Prov is missing or not an inductive type"
  -- 3. Vocab
  let some sinfo := getStructureInfo? env vocabN | err "Vocab is not a structure"; return (← errs.get)
  let projs := sinfo.fieldNames.toList.map (vocabN ++ ·)
  let c : Ctx := { projs }
  let some (.inductInfo fi) := env.find? (A "Field") | err "Field is not an inductive type"; return (← errs.get)
  if fi.numParams != 0 || fi.numIndices != 0 then err "Field must have no parameters or indices"
  for ctor in fi.ctors do
    if let some (.ctorInfo ci) := env.find? ctor then
      if ci.numFields != 0 then err s!"Field constructor {ctor} must take no arguments"
  withLocalDeclD `v (mkConst vocabN) fun v => do
    let mut earlier : Array Expr := #[]
    for f in sinfo.fieldNames do
      let p := mkApp (mkConst (vocabN ++ f)) v
      let t ← instantiateMVars (← inferType p)
      let natOrInt (d : Expr) : Bool := d.isConstOf ``Nat || d.isConstOf ``Int
      let ok ← if t.isSort then pure (t == mkSort Level.zero || t == mkSort Level.one)
        else if natOrInt t || earlier.contains t then pure true
        else if t.isForall then
          forallTelescope t fun xs body => do
            let doms ← xs.mapM fun x => inferType x
            pure (body == mkSort Level.zero && doms.all (fun d => natOrInt d || earlier.contains d))
        else pure false
      unless ok do err s!"Vocab field {f} has a disallowed type (atoms, Nat/Int, predicates and carrier elements only)"
      if t == mkSort Level.one then earlier := earlier.push p
      if (← findDocString? env (vocabN ++ f)).isNone then err s!"Vocab field {f} has no doc comment"
    -- 4. premises
    for ctor in fi.ctors do
      let cname := match ctor with | .str _ s => s | _ => ctor.toString
      let doc := oneLine ((← findDocString? env ctor).getD "")
      let pv ← whnf (mkApp (mkConst (A "prov")) (mkConst ctor))
      let provS := match pv.getAppFn with
        | .const n _ => match n with | .str _ s => s | _ => "?"
        | _ => "?"
      let app := mkApp2 (mkConst (A "prem")) (mkConst ctor) v
      let body ← match ← unfoldDefinition? app with
        | some e => reduceMatch e
        | none => pure app
      let body ← instantiateMVars body
      let forbidden := (constsOf body).filter (fun n => !(projs.contains n || allowedConsts.contains n))
      let num := match numForm? c body with
        | some (op, val) => s!"{op}:{val}"
        | none => "none"
      let hasProj := (constsOf body).any projs.contains
      let bodyS := oneLine (toString (← ppExpr body))
      IO.println s!"PREMISE {cname} | prov={provS} | head={headOf body} | literal={isLiteral c body} | proj={hasProj} | num={num} | forbidden={forbidden} | body={bodyS} | doc={doc}"
    -- 5. Conclusion
    match ← unfoldDefinition? (mkApp (mkConst (A "Conclusion")) v) with
    | some cb =>
      let cb := cb.headBeta
      let forbidden := (constsOf cb).filter (fun n => !(projs.contains n || allowedConsts.contains n))
      let doc := oneLine ((← findDocString? env (A "Conclusion")).getD "")
      let bodyS := oneLine (toString (← ppExpr cb))
      IO.println s!"CONCLUSION | head={headOf cb} | literal={isLiteral c cb} | proj={(constsOf cb).any projs.contains} | forbidden={forbidden} | body={bodyS} | doc={doc}"
    | none => err "Conclusion is not a definition"
  -- 6. fixed block B, pinned by definitional value
  let hdr := [("Premises", "fun (v : Vocab) => ∀ f, prem f v"),
              ("Without", "fun (g : Field) (v : Vocab) => ∀ f, _root_.Ne f g → prem f v"),
              ("Stated", "fun (v : Vocab) => ∀ f, _root_.Eq (prov f) Prov.stated → prem f v"),
              ("Explicit", "fun (v : Vocab) => ∀ f, _root_.Ne (prov f) Prov.reconstructed → prem f v")]
  for (n, s) in hdr do
    match env.find? (A n) with
    | some (.defnInfo d) =>
      let want ← elabStr s
      unless d.value == want do err s!"fixed block B: {n} differs from the template"
    | _ => err s!"fixed block B: {n} is missing"
  -- 7. pinned theorem statements
  let check (thm stmt : String) : TermElabM Bool := do
    match env.find? (A thm) with
    | none => pure false
    | some ci =>
      let want ← elabStr stmt
      unless ci.type == want do err s!"{thm} has the wrong statement; expected: {stmt}"
      pure true
  for (thm, stmt) in [("final", "∀ v, Premises v → Conclusion v"),
                      ("final_nontrivial", "_root_.Not (∀ v : Vocab, Conclusion v)"),
                      ("consistent", "_root_.Exists (fun v => Premises v)"),
                      ("alone_insufficient", "∀ g, _root_.Not (∀ v, prem g v → Conclusion v)")] do
    unless (← check thm stmt) do err s!"missing required theorem {thm}"
  let ctorNames := fi.ctors.map (fun n => match n with | .str _ s => s | _ => "")
  for cn in ctorNames do
    let a ← check s!"{cn}_needed" s!"_root_.Not (∀ v, Without Field.{cn} v → Conclusion v)"
    let b ← check s!"{cn}_redundant" s!"∀ v, Without Field.{cn} v → Conclusion v"
    if a == b then err s!"premise {cn} needs exactly one of {cn}_needed / {cn}_redundant"
  for (pre, defn) in [("stated", "Stated"), ("explicit", "Explicit")] do
    let a ← check s!"{pre}_sufficient" s!"∀ v, {defn} v → Conclusion v"
    let b ← check s!"{pre}_insufficient" s!"_root_.Not (∀ v, {defn} v → Conclusion v)"
    if a == b then err s!"exactly one of {pre}_sufficient / {pre}_insufficient is required"
  -- 8. orphan _needed / _redundant theorems
  for n in names do
    if n.getPrefix != ns then continue
    let s := match n with | .str _ s => s | _ => ""
    for suf in ["_needed", "_redundant"] do
      if s.endsWith suf then
        let base := String.ofList (s.toList.take (s.length - suf.length))
        unless ctorNames.contains base do err s!"{s} does not correspond to a premise"
  errs.get

def main : IO Unit := do
  initSearchPath (← findSysroot)
  let sp ← searchPathRef.get
  searchPathRef.set (sp ++ [System.FilePath.mk ".lake/build/lib/lean"])
  let env ← importModules #[{module := ns}] {}
  let ctx : Core.Context := { fileName := "<audit>", fileMap := default, currNamespace := ns,
                              openDecls := [.simple ns []] }
  let st : Core.State := { env }
  let r ← ((audit.run' {} {}).run' {} {} |>.toIO ctx st).toBaseIO
  match r with
  | .ok (errs, _) =>
    for e in errs do IO.println s!"ERROR: {e}"
    IO.println (if errs.isEmpty then "AUDIT_OK" else "AUDIT_FAILED")
  | .error e =>
    IO.println s!"ERROR: audit crashed: {e}"
    IO.println "AUDIT_FAILED"

#eval main
