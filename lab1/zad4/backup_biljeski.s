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
.LFB0: ; lokalna labela
	.cfi_startproc ; pocetak nove procedure (funkcije)
	endbr64 ; https://stackoverflow.com/questions/56905811/what-does-the-endbr64-instruction-actually-do
	push	rbp ; stavlja sadrzaj registra rbp (base pointer) na stog
	.cfi_def_cfa_offset 16 ; offset za 16 od mjesta CFA (Canonical Frame Pointer = vrijednost stack pointera prije CALL instrukcije roditeljske funkcije) na koje pokazuje stack pointer (rsp) https://stackoverflow.com/questions/7534420/gas-explanation-of-cfi-def-cfa-offset
	.cfi_offset 6, -16 ; sprema prethodnu vrijednost REGISTRA (6 ili rbp) offsetanu za -16 od CFA 
	mov	rbp, rsp ; pomice sadrzaj registra rsp (stack pointer; pokazuje na vrh) u rbp (pokazuje na dno)
	.cfi_def_cfa_register 6 ; CFA je registar 6 (rbp) sad https://stackoverflow.com/questions/2529185/what-are-cfi-directives-in-gnu-assembler-gas-used-for 
	mov	QWORD PTR -8[rbp], rdi ; rsi - registar prvog funkc. arg. https://www.cs.uaf.edu/2017/fall/cs301/lecture/09_11_registers.html ; sadrzaj rdi-ja stavljamo na mjesto rbp-8 i tretiramo kao adresu https://reverseengineering.stackexchange.com/questions/10746/what-does-mov-qword-ptr-dsrax18-r8-mean 
	mov	DWORD PTR -12[rbp], esi ; drugi argument fje(?); sadrzaj esi-ja stavljamo 
	mov	rax, QWORD PTR -8[rbp] ; ucitavanje 
	mov	edx, DWORD PTR -12[rbp]
	mov	DWORD PTR [rax], edx
	nop
	pop	rbp
	.cfi_def_cfa 7, 8
	ret ; CPU naredbe
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
	mov	QWORD PTR -8[rbp], rdi
	mov	DWORD PTR -12[rbp], esi
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, DWORD PTR -12[rbp]
	mov	DWORD PTR 8[rax], edx
	nop
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
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
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	mov	QWORD PTR -8[rbp], rdi
	lea	rdx, vtable for Base[rip 16]
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx
	nop
	pop	rbp
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
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	Base::Base()
	lea	rdx, vtable for CoolClass[rip 16]
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx
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
	call	_Znwm@PLT
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