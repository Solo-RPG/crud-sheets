package com.solo.rpg.sheetservice.model;

public class SheetData {
    private String campo;
    private SheetFieldValue valor;

    public SheetData(String campo, SheetFieldValue valor) {
        this.campo = campo;
        this.valor = valor;
    }

    public String getCampo() {
        return campo;
    }

    public void setCampo(String campo) {
        this.campo = campo;
    }

    public SheetFieldValue getValor() {
        return valor;
    }

    public void setValor(SheetFieldValue valor) {
        this.valor = valor;
    }
}
