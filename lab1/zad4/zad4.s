.file	"zad4.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.PlainOldClass::set(int),"axG",@progbits,PlainOldClass::set(int),comdat
	.align 2
	.weak	PlainOldClass::set(int)
	.type	PlainOldClass::set(int), @function
PlainOldClass::set(int):
; https://stackoverflow.com/questions/15284947/understanding-gcc-s-output 
; https://sourceware.org/binutils/docs/as/CFI-directives.html
; https://www.cs.uaf.edu/2017/fall/cs301/lecture/09_11_registers.html
.LFB0: ; lokalna labela
	.cfi_startproc ; pocetak nove procedure (funkcije)
	endbr64 ; https://stackoverflow.com/questions/56905811/what-does-the-endbr64-instruction-actually-do
	push	rbp ; (1) stavlja sadrzaj registra rbp (base pointer) na stog
	.cfi_def_cfa_offset 16 ; (2) offset za 16 od mjesta CFA (Canonical Frame Pointer = vrijednost stack pointera prije CALL instrukcije roditeljske funkcije) na koje pokazuje stack pointer (rsp) https://stackoverflow.com/questions/7534420/gas-explanation-of-cfi-def-cfa-offset
	.cfi_offset 6, -16 ; (3) sprema prethodnu vrijednost REGISTRA (6 ili rbp) offsetanu za -16 od CFA
	mov	rbp, rsp ; (4) pomice sadrzaj registra rsp (stack pointer; pokazuje na vrh) u rbp (pokazuje na dno)
	.cfi_def_cfa_register 6 ; (5) Call Frame Adress je registar 6 (rbp) tj. adresa povratka iz fje  https://stackoverflow.com/questions/2529185/what-are-cfi-directives-in-gnu-assembler-gas-used-for 
	mov	QWORD PTR -8[rbp], rdi ; (6) rdi - registar koji se koristi za 1. argument fje; citamo vrijednosti s adrese [rbp-8] https://www.cs.uaf.edu/2017/fall/cs301/lecture/09_11_registers.html ; sadrzaj rdi-ja stavljamo na mjesto rbp-8 i tretiramo kao adresu https://reverseengineering.stackexchange.com/questions/10746/what-does-mov-qword-ptr-dsrax18-r8-mean 
	mov	DWORD PTR -12[rbp], esi ; (7) esi - registar koji se koristi za 2. argument fje ; sadrzaj esi-ja stavljamo 
	mov	rax, QWORD PTR -8[rbp] ; (8) rax - registar pomocu kojeg se fje vracaju iz funkcija; stavljamo sadrzan s adrese rbp-8 u rax (valjda 1. argument fje) ; https://www.cs.uaf.edu/2017/fall/cs301/lecture/09_11_registers.html
	mov	edx, DWORD PTR -12[rbp] ; (9) stavljamo sadrzaj s adrese rbp-12 u edx (valjda 2. argument fje)
	mov	DWORD PTR [rax], edx ; (9) stavljamo sadrzaj iz registra edx na adresu na koju pokazuje rax ()
	nop ; no operation
	pop	rbp ; pop-a se vrh stoga (sadrzaj rbp-a na pocetku svega)
	.cfi_def_cfa 7, 8 ; pravilo za racunanje CFA, uzima adresu iz registra (7) i dodaje offset (+8) na to
	ret ; kraj procedure; popa sa stoga adresu i bezuvjetno skace tamo  https://cs.brown.edu/courses/cs033/docs/guides/x64_cheatsheet.pdf
	.cfi_endproc
.LFE0:
	.size	PlainOldClass::set(int), .-PlainOldClass::set(int)
	.section	.text.CoolClass::set(int),"axG",@progbits,CoolClass::set(int),comdat
	.align 2
	.weak	CoolClass::set(int)
	.type	CoolClass::set(int), @function
CoolClass::set(int):
.LFB2:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	QWORD PTR -8[rbp], rdi ; this pointer spremamo na adresu -8[rbp] jer 
	mov	DWORD PTR -12[rbp], esi ; spremamo vrijednost int-a iz registra esi na adresu -12[rbp]
	mov	rax, QWORD PTR -8[rbp] ; loadamo this pointer u rax registar (int)
	mov	edx, DWORD PTR -12[rbp] ; loadamo int vrijednost u edx registar 
	mov	DWORD PTR 8[rax], edx ; spremamo vrijednost registra edx na adresu na koju pokazuje this 
	nop ; no operation
	pop	rbp ; micemo rbp sa stoga ()
	.cfi_def_cfa 7, 8
	ret ;
	.cfi_endproc
.LFE2:
	.size	CoolClass::set(int), .-CoolClass::set(int)
	.section	.text.CoolClass::get(),"axG",@progbits,CoolClass::get(),comdat
	.align 2
	.weak	CoolClass::get()
	.type	CoolClass::get(), @function
CoolClass::get():
.LFB3:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	QWORD PTR -8[rbp], rdi
	mov	rax, QWORD PTR -8[rbp]
	mov	eax, DWORD PTR 8[rax]
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	CoolClass::get(), .-CoolClass::get()
	.section	.text.Base::Base(),"axG",@progbits,Base::Base(),comdat
	.align 2
	.weak	Base::Base()
	.type	Base::Base(), @function
Base::Base():
.LFB7:
	.cfi_startproc
	endbr64
	push	rbp ; stavljamo rbp na stog (base pointer register)
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp ; micemo vrijednost stack pointera u rbp
	.cfi_def_cfa_register 6 
	mov	QWORD PTR -8[rbp], rdi ; adresa na koju pokazuje this
	lea	rdx, vtable for Base[rip 16] ; loadamo ADRESU vtable-a klase Base sa adrese rip+16 (rip - registar posebne namjene, sadrzi adresu sljedece instrukcije koju trebamo izvrsit) https://cs.brown.edu/courses/csci1310/2020/notes/l08.html
	mov	rax, QWORD PTR -8[rbp] ; spremamo adresu this-a u registar rax
	mov	QWORD PTR [rax], rdx ; spremi adresu vtable-a na mjesto u memoriji gdje pokazuje rax
	nop
	pop	rbp ; restore-a vrijednost rbp-a prije poziva funkcije https://www.cs.uaf.edu/2010/fall/cs301/lecture/10_06_the_stack.html
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	Base::Base(), .-Base::Base()
	.weak	Base::Base()
	.set	Base::Base(),Base::Base()
	.section	.text.CoolClass::CoolClass(),"axG",@progbits,CoolClass::CoolClass(),comdat
	.align 2
	.weak	CoolClass::CoolClass()
	.type	CoolClass::CoolClass(), @function
CoolClass::CoolClass():
.LFB9:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp ; spremamo rsp u rbp registar
	.cfi_def_cfa_register 6
	sub	rsp, 16 ; oduzimamo od rsp 16 (za vptr i int x_)
	mov	QWORD PTR -8[rbp], rdi ; loadamo prvi argument (this)
	mov	rax, QWORD PTR -8[rbp] ; loadamo this pointer u rax
	mov	rdi, rax ; prebacujemo this pointer u rdi
	call	Base::Base() ; zovemo konstruktor Base klase
	lea	rdx, vtable for CoolClass[rip 16] ; loadamo vtablea u rdxs
	mov	rax, QWORD PTR -8[rbp] ; spremamo adresu na koju pokazuje this pointer u rax
	mov	QWORD PTR [rax], rdx ; pomicemo spremamo adresu vtablea na mjeso gdje pkazuje rax (this pointer)
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	CoolClass::CoolClass(), .-CoolClass::CoolClass()
	.weak	CoolClass::CoolClass()
	.set	CoolClass::CoolClass(),CoolClass::CoolClass()
	.text
	.globl	main
	.type	main, @function
main:
.LFB4:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	push	rbx
	sub	rsp, 40
	.cfi_offset 3, -24
	mov	rax, QWORD PTR fs:40
	mov	QWORD PTR -24[rbp], rax
	xor	eax, eax
	mov	edi, 16
	call	_Znwm@PLT ; operator new(unsigned long)
	mov	rbx, rax
	mov	rdi, rbx
	call	CoolClass::CoolClass()
	mov	QWORD PTR -32[rbp], rbx
	lea	rax, -36[rbp]
	mov	esi, 42
	mov	rdi, rax
	call	PlainOldClass::set(int)
	mov	rax, QWORD PTR -32[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR -32[rbp]
	mov	esi, 42
	mov	rdi, rax
	call	rdx
	mov	eax, 0
	mov	rcx, QWORD PTR -24[rbp]
	xor	rcx, QWORD PTR fs:40
	je	.L9
	call	__stack_chk_fail@PLT
.L9:
	add	rsp, 40
	pop	rbx
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	main, .-main
	.weak	vtable for CoolClass
	.section	.data.rel.ro.local.vtable for CoolClass,"awG",@progbits,vtable for CoolClass,comdat
	.align 8
	.type	vtable for CoolClass, @object
	.size	vtable for CoolClass, 32
vtable for CoolClass:
	.quad	0
	.quad	typeinfo for CoolClass
	.quad	CoolClass::set(int)
	.quad	CoolClass::get()
	.weak	vtable for Base
	.section	.data.rel.ro.vtable for Base,"awG",@progbits,vtable for Base,comdat
	.align 8
	.type	vtable for Base, @object
	.size	vtable for Base, 32
vtable for Base:
	.quad	0
	.quad	typeinfo for Base
	.quad	__cxa_pure_virtual
	.quad	__cxa_pure_virtual
	.weak	typeinfo for CoolClass
	.section	.data.rel.ro.typeinfo for CoolClass,"awG",@progbits,typeinfo for CoolClass,comdat
	.align 8
	.type	typeinfo for CoolClass, @object
	.size	typeinfo for CoolClass, 24
typeinfo for CoolClass:
	.quad	vtable for __cxxabiv1::__si_class_type_info 16
	.quad	typeinfo name for CoolClass
	.quad	typeinfo for Base
	.weak	typeinfo name for CoolClass
	.section	.rodata.typeinfo name for CoolClass,"aG",@progbits,typeinfo name for CoolClass,comdat
	.align 8
	.type	typeinfo name for CoolClass, @object
	.size	typeinfo name for CoolClass, 11
typeinfo name for CoolClass:
	.string	"9CoolClass"
	.weak	typeinfo for Base
	.section	.data.rel.ro.typeinfo for Base,"awG",@progbits,typeinfo for Base,comdat
	.align 8
	.type	typeinfo for Base, @object
	.size	typeinfo for Base, 16
typeinfo for Base:
	.quad	vtable for __cxxabiv1::__class_type_info 16
	.quad	typeinfo name for Base
	.weak	typeinfo name for Base
	.section	.rodata.typeinfo name for Base,"aG",@progbits,typeinfo name for Base,comdat
	.type	typeinfo name for Base, @object
	.size	typeinfo name for Base, 6
typeinfo name for Base:
	.string	"4Base"
	.ident	"GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4: