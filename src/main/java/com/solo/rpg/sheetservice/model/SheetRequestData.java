package com.solo.rpg.sheetservice.model;

public class SheetRequestData {
    private String campo;
    private Object valor;

    public SheetRequestData(String campo, Object valor) {
        this.campo = campo;
        this.valor = valor;
    }

    public String getCampo() {
        return campo;
    }

    public void setCampo(String campo) {
        this.campo = campo;
    }

    public Object getValor() {
        return valor;
    }

    public void setValor(Object object) {
        this.valor = object;
    }
}
